from typing import Dict, List, Optional
from bs4 import BeautifulSoup


def parse_schema_names_options(html_parsed_content: BeautifulSoup) -> Dict[str, str]:
    """parse and return schema names dictionary with value"""

    schema_names = {}
    options = html_parsed_content.find("select", {'name': "schemaname"}).find_all('option')
    first = True

    for option in options:
        if first:
            first = False
            continue
        schema_names[option.text] = option['value']

    return schema_names


def parse_detailed_info_urls_list(html_parsed_content: BeautifulSoup) -> List[str]:
    """parse and return list of detailed info urls"""

    detailed_info_list = []

    table = html_parsed_content.find("div", {'class': 'col-md-12'}).find('table').find_all('a', href=True)
    for item in table:
        detailed_info_list.append(item['href'].split("'")[1])

    return detailed_info_list


def parse_detailed_table_data(html_parsed_content:BeautifulSoup) -> Optional[Dict[str, str]]:
    """parse and return detailed case info"""

    case_detail = {}

    try:
        table_data = html_parsed_content.find_all('table')[0].find_all('tr')

        for tr in table_data:

            if tr.find('td'):
                tds = tr.find_all('td')

                if len(tds) == 2:
                    blink = tds[1].find('blink')

                    if blink:
                        case_detail[tds[0].text.strip()] = blink.text.strip()
                    else:
                        case_detail[tds[0].text.strip()] = tds[1].text.strip()

    except Exception as ex:
        print(f"could not parse data, err: {ex}")
        return None

    return case_detail


def parse_html_content(html_content: bytes):
    """Helper function to parse html"""
    return BeautifulSoup(html_content, 'html5lib')
