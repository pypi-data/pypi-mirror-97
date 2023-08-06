from __future__ import unicode_literals
import itertools
import re
import ipaddress
import iocextract
from builtins import str
import json
import os


class IOCParser(object):
    
    @staticmethod
    def unravel(value, wrap_chars):
        to_return = []
        for i in range(0, len(wrap_chars)):
            wrapping_char = wrap_chars[i]
            re_str = r"\{start}([^<>\[\]\(\)]*)\{end}".format(start=wrapping_char[0], end=wrapping_char[1])
            match = re.compile(re_str)
            match = match.findall(value)
            if match:
                to_return.extend(match)
            else:
                continue

        to_return.append(value)
        return to_return

    def possible_entries(self, entry):
        # Text that might wrap an IOC, in format <start txt>, <end txt>
        # So for example "(10.20.32.123)" -> "10.20.32.123"

        wrapping_chars = [  # Will be recursed on, so only add static regex
            ("(", ")"),
            ("<", ">"),
            (";", ";"),
            ("[", "]"),
            ("-", "-"),
            ('"', '"')
        ]

        sub_entries = self.unravel(entry, wrapping_chars)

        wrapping_txts = [
            (";", ";"),
            ("href=\"", "\""),
            ("alt=\"", "\""),
            ("<", ">,"),
        ]

        poss = []
        poss.extend(sub_entries)
        poss.append(entry)

        sub_strings = re.split("[<>]", entry)
        poss.extend(sub_strings)

        for start_txt, end_txt in wrapping_txts:
            starts_w = entry.startswith(start_txt)
            ends_w = entry.endswith(end_txt)

            if starts_w:
                poss.append(entry[len(start_txt):])

            if ends_w:
                poss.append(entry[:-len(end_txt)])

            if starts_w and ends_w:
                poss.insert(0, entry[len(start_txt):-len(end_txt)])  # Insert to beginning because of stripping

        return poss

    def parse_iocs(self, text, defang=False,  whitelist_regex=''):

        ioc_typer = IOCTyper()
        # emails will often enforce strict line limits, so IOCs can be split in half by a newline.
        # remove all linebreaks to avoid this issue.
        text2 = re.sub("[\n\r]+", "", text)
        text_chunks = set()
        for text_input in [text, text2]:
            split_text = re.split(r"(\n| )", text_input)
            split_text = map(lambda x: x.strip("\r\t\n "), split_text)
            split_text = filter(lambda x: len(x) > 2, split_text)  # Strip out single chars
            text_chunks.update(split_text)

        entries = []

        for entry in text_chunks:
            # Each entry might not be split correctly, try some combinations
            for pos in self.possible_entries(entry):
                typ = ioc_typer.type_ioc(pos)

                if typ != "unknown":
                    entries.append((pos, typ))

        # iocextract can find iocs that have been defanged.  They are refanged and added to the correct type.
        # Patched: iocextract has bug in yara regex for long strings causing exponential back string matches.
        # This chain call is the same as extract_iocs except yara is removed.  We tried doing a timeout on
        # the call that searched for yara, but the timeout wrapper wasn't windows compatible.
        iocs = set(itertools.chain(
            iocextract.extract_urls(text, refang=True, strip=False),
            iocextract.extract_ips(text, refang=True),
            iocextract.extract_emails(text, refang=True),
            iocextract.extract_hashes(text),
        ))

        for ioc in iocs:
            typ = ioc_typer.type_ioc(ioc)
            entries.append((ioc, typ))
            for pos in self.possible_entries(ioc):
                typ = ioc_typer.type_ioc(pos)
                if typ != "unknown":
                    entries.append((pos, typ))

        result = IOCTyper.build_empty_ioc_dict()

        for entry, typ in entries:
            result[typ].append(entry)

        # Append domains from URLs to the domains result
        cleaned_urls = [re.sub("https?(://)?", "", u) for u in result["url"]]  # Strip schema
        cleaned_urls = [re.sub("[/?].*", "", u) for u in cleaned_urls]  # Strip excess /'s

        domain_validator = DomainIOC()
        for cleaned_url in cleaned_urls:
            if domain_validator.run(cleaned_url, check_tld=False):
                result["domain"].append(cleaned_url)

        # Remove duplicates
        for k, v in result.items():
            result[k] = list(set(v))

        # Clear results based on whitelist
        if whitelist_regex:
            for ioc_typ in IOCTyper.IOC_TYPES:
                ioc_list = []
                for ioc in result[ioc_typ]:
                    if re.findall(whitelist_regex, ioc):
                        pass  # Found match, don't add to list
                    else:
                        ioc_list.append(ioc)
                result[ioc_typ] = ioc_list
        if defang:
            result = self.defang_results(result)
        return result

    @staticmethod
    def defang_results(results):
        defangable = ['domain', 'ipv4_private', 'ipv4_public', 'url']
        new_results = {}
        for key, value in results.items():
            if key in defangable:
                new_value = []
                for ioc in value:
                    new_value.append(iocextract.defang(ioc))
                new_results[key] = new_value
        results.update(new_results)
        return results

class IOCTyper(object):
    # Order of this list determnines the detection order, DO NOT CHANGE
    # Add new types to the top of this list
    IOC_TYPES = [
        'ssdeep',
        'sha256',
        'sha1',
        'md5',
        'email',
        'ipv4_public',
        'ipv4_private',
        'ipv6_public',
        'ipv6_private',
        'filename',
        'domain',
        'url',
        'unknown'
    ]

    COMMON_FILETYPES = ['3dm', '3ds', '3g2', '3gp', '7z', 'accdb', 'ai', 'aif', 'apk', 'app', 'asf', 'asp',
                        'aspx', 'avi', 'b', 'bak', 'bat', 'bin', 'bmp', 'c', 'cab', 'cbr', 'cer', 'cfg',
                        'cfm', 'cgi', 'class', 'cpl', 'cpp', 'crdownload', 'crx', 'cs', 'csr', 'css',
                        'csv', 'cue', 'cur', 'dat', 'db', 'dbf', 'dcr', 'dds', 'deb', 'dem', 'deskthemepack',
                        'dll', 'dmg', 'dmp', 'doc', 'docm', 'docx', 'download', 'drv', 'dtd', 'dwg', 'dxf',
                        'eps', 'exe', 'fla', 'flv', 'fnt', 'fon', 'gadget', 'gam', 'ged', 'gif', 'gpx', 'gz',
                        'h', 'hqx', 'htm', 'html', 'icns', 'ico', 'ics', 'iff', 'indd', 'ini', 'iso', 'jar',
                        'java', 'jpeg', 'jpg', 'js', 'json', 'jsp', 'key', 'keychain', 'kml', 'kmz', 'lnk',
                        'log', 'lua', 'm', 'm3u', 'm4a', 'm4v', 'max', 'mdb', 'mdf', 'mid', 'mim', 'mov',
                        'mp3', 'mp4', 'mpa', 'mpeg', 'mpg', 'msg', 'msi', 'nes', 'obj', 'odt', 'otf',
                        'pages', 'part', 'pct', 'pdb', 'pdf', 'php', 'pkg', 'pl', 'plugin', 'png', 'pps',
                        'ppt', 'pptx', 'prf', 'ps', 'psd', 'pspimage', 'py', 'rar', 'rm', 'rom', 'rpm',
                        'rss', 'rtf', 'sav', 'sdf', 'sh', 'sitx', 'sln', 'sql', 'srt', 'svg', 'swf', 'swift',
                        'sys', 'tar', 'tax2016', 'tax2017', 'tex', 'tga', 'thm', 'tif', 'tiff', 'tmp',
                        'toast', 'torrent', 'ttf', 'txt', 'uue', 'vb', 'vcd', 'vcf', 'vcxproj', 'vob', 'wav',
                        'wma', 'wmv', 'wpd', 'wps', 'wsf', 'xcodeproj', 'xhtml', 'xlr', 'xls', 'xlsx',
                        'xlsm', 'xml', 'yuv', 'zip', 'zipx', 'webm', 'flac', 'numbers']


    URL_REGEX_COMPILED = re.compile(r"""^                                    #beginning of line	
(?P<proto>https?:\/\/)               #protocol                http://	
(	
(?P<domain>(([\u007E-\uFFFFFF\w-]+[.])+[\u007E-\uFFFFFF\w-]{2,}))	
|	
(?P<ipv4>(?:(?:\b|\.)(?:2(?:5[0-5]|[0-4]\d)|1?\d?\d)){4})	
|	
(\[?	
(?P<ipv6>(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])))	
\]?)	
)	
(?P<port>:\d{1,5})?	
\/?                                    #domain                    www.google.co.uk	
(?P<directory>(?<=\/)([{}%|~\/!?A-Za-z0-9_.-]+)(?=\/))?                    #directory    /var/www/html/apps	
\/?                                    #final directory slash    /	
(?P<filename>([^?<>"]+))?                #filename                index.php	
                                    #query marker            ?	
(?P<query>\?[^\s"<>]*)?                        #query text                cmd=login_submit&id=1#cnx=2.123	
$                                    #end of line""", re.VERBOSE | re.UNICODE)

    FILE_REGEX = r'^(?!.*[\\/:*"<>|])[\w !@#$%^&*()+=\[\]{}\'"-]+(\.[\w -]+)?$'

    def __init__(self):
        self.ioc_patterns = {
            'ipv4_public': IPv4PublicIOC(),
            'ipv4_private': IPv4PrivateIOC(),
            'ipv6_public': IPv6PublicIOC(),
            'ipv6_private': IPv6PrivateIOC(),

            'url': URLIOC(self),
            'email': RegexIOC(r'^[\w%+.-]+@[A-Za-z0-9.-]+\.[a-z]{2,}$'),
            'md5': RegexIOC(r'^[a-fA-F0-9]{32}$'),
            'sha1': RegexIOC(r'^[a-fA-F0-9]{40}$'),
            'sha256': RegexIOC(r'^[a-fA-F0-9]{64}$'),
            'ssdeep': RegexIOC(r'^([1-9]\d*)(?!:\d\d($|:)):([\w+0-9\/]+):([\w+0-9\/]+)$')
        }

        self.ioc_patterns.update({
            'filename': FilenameIOC(IOCTyper.FILE_REGEX),
            'domain': DomainIOC(),
            'unknown': AnyIOC()
        })

        self.tld_patterns = {
            'validSLD': re.compile(r'^[a-z0-9-]+$', re.IGNORECASE),
            'validTLD': re.compile(r'^[a-z]{2,64}$'),
            'tld': re.compile(r'^\.[a-z]{2,}$')
        }

    @staticmethod
    def build_empty_ioc_dict():
        iocs = {}
        for ioc in IOCTyper.IOC_TYPES:
            iocs[ioc] = []

        return iocs

    def is_ip(self, value):
        versions = ["4", "6"]
        p_levels = ["public", "private"]
        for v in versions:
            for p_level in p_levels:
                if self.ioc_patterns["ipv{}_{}".format(v, p_level)].run(value):
                    return True
        return False

    def type_ioc(self, ioc):
        for pat_name in IOCTyper.IOC_TYPES:
            if self.ioc_patterns[pat_name].run(ioc):
                return pat_name


class IOCObj(object):
    def run(self, value):
        raise NotImplementedError


class AnyIOC(IOCObj):  # Always returns true
    def run(self, value):
        return True


class RegexIOC(object):
    def __init__(self, regex, re_flags=0):
        """
        :param regex: Regex String to match a value against
        """
        self.regex = re.compile(regex, re_flags)

    def run(self, value):
        return bool(self.regex.search(value))


class URLIOC(IOCObj):
    def __init__(self, typer):
        self.typer = typer

    def run(self, value):
        match = IOCTyper.URL_REGEX_COMPILED.search(value)
        if match and len(match.group()) == len(value):
            return True
        return False


class FilenameIOC(IOCObj):
    def __init__(self, regex):
        self.regex = re.compile(regex)

    def run(self, value):
        match = self.regex.search(value)
        if match and self.is_filename(match.group()):
            return True
        return False

    @staticmethod
    def is_filename(fn):

        extension = ".".join(fn.split(".")[-1:])
        if extension == fn:
            return False

        if extension in IOCTyper.COMMON_FILETYPES:
            return True
        else:
            return False


class DomainIOC(IOCObj):
    NUMERIC_NOT_A_DOMAIN = numeric_only = re.compile(r'^([0-9]+\.)+[0-9]+$')
    GENERAL_DOMAIN = re.compile(r'(([\u007E-\uFFFFFF\w-]+[.])+[\u007E-\uFFFFFF\w-]{2,})', re.UNICODE)
    with open(os.path.join(os.path.dirname(__file__), 'data/tld_list.json'), 'r') as f:
        COMMON_TLDS = json.load(f)

    def ends_with_tld(self, domain):
        for tld in self.COMMON_TLDS:
            if domain.split('.')[-1].lower() == tld.lower():
                return True
        return False

    def run(self, value, check_tld=True):
        match = self.GENERAL_DOMAIN.search(value)
        if match and len(match.group()) == len(value):
            bad_match = self.NUMERIC_NOT_A_DOMAIN.search(value)
            if not bad_match or len(bad_match.group()) != len(value):
                if check_tld:
                    if self.ends_with_tld(value):
                        return True
                else:
                    return True

        return False


class IPIOC(IOCObj):
    def privacy_valid(self, value):
        # Return true if the value is private otherwise false if public
        ipaddr = ipaddress.ip_address(str(value))
        if ipaddr.is_private == self.is_private():
            return True
        else:
            return False

    def is_private(self):
        # Return true if the ioc typer is for private ips only else false for public
        raise NotImplementedError

    def ip_ver(self):
        # Return ip version, either 4 or 6
        raise NotImplementedError

    def ioc_name(self):
        # Returns one of ipv6_private, ipv6_public, ipv4_public, ipv4_private
        name = "ipv{}".format(self.ip_ver())
        name += "_{}".format("private" if self.is_private() else "public")
        return name

    def get_regex(self):
        raise NotImplementedError

    def __init__(self):
        self.regex = re.compile(self.get_regex())

    def run(self, value):
        match = self.regex.search(value)
        result = False

        try:
            ipaddress.ip_address(str(value))  # Try parsing IP
        except ValueError:
            return False

        if match:
            result = True and self.privacy_valid(value)

        return result


class IPv4PublicIOC(IPIOC):
    def get_regex(self):
        return r'^(?:(?:\b|\.)(?:2(?:5[0-5]|[0-4]\d)|1?\d?\d)){4}$'

    # Keeping regex in case it becomes useful
    #         # Class A
    #         r'^10\.(2([0-5]{2})|2[0-9]{1}|1?\d?\d)\.(2([0-5]{2})|2[0-9]{1}|1?\d?\d)\.(2([0-5]{2})|2[0-9]{1}|1?\d?\d)$',
    #         # Class B
    #         r'^172\.(3([01])|1[6-9]|2\d)\.(2([0-5]{2})|2[0-9]{1}|1?\d?\d)\.(2([0-5]{2})|2[0-9]{1}|1?\d?\d)$',
    #         # Class C
    #         r'^192\.168\.(2([0-5]{2})|2[0-9]{1}|1?\d?\d)\.(2([0-5]{2})|2[0-9]{1}|1?\d?\d)$',
    #     ]

    def is_private(self):
        return False

    def ip_ver(self):
        return "4"


class IPv4PrivateIOC(IPv4PublicIOC):
    def is_private(self):
        return True


class IPv6PublicIOC(IPIOC):
    def get_regex(self):
        return r'^(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))$'

    def is_private(self):
        return False

    def ip_ver(self):
        return "6"


class IPv6PrivateIOC(IPv6PublicIOC):
    def is_private(self):
        return True
