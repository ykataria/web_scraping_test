from typing import List

import requests
from requests.exceptions import RequestException

from web_scraping_test.utils.parse_captcha_image import get_number_from_captcha_image
from web_scraping_test.utils import parse_html_data as p_html
from web_scraping_test.utils.parse_html_data import parse_html_content
from web_scraping_test.utils.save_case_data import save_case_data_in_excel_and_csv


HEADERS = {
    'user-agent': 'Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, likeGecko) Chrome/102.0.0.0 '
                  'Safari/537.36 '
}
BASE_URL = "https://drt.gov.in/front/page1_advocate.php"


def get_site_meta_data():
    """function to fetch captcha, schema name and cookies"""

    session = requests.Session()

    try:
        resp = session.get(BASE_URL, headers=HEADERS)

        # parse html into bs4 object
        parsed_content = parse_html_content(resp.content)

        # get schema data from the retrieved html data
        schema_data = p_html.parse_schema_names_options(parsed_content)

        # download captcha image
        captcha_response = session.get('https://drt.gov.in/front/captcha.php')
        with open("captcha_data/captcha.png", 'wb') as f:
            f.write(captcha_response.content)
        captcha_number = get_number_from_captcha_image()

        return session, schema_data, captcha_number

    except RequestException as re:
        print(f"exception raised while sending request: {re}")
    except Exception as ex:
        print(ex)


def fetch_detailed_case_info_urls(
        session: requests.Session,
        captcha_number: str,
        schema_name: int,
        party_name: str
):
    """fetch the detailed info from the passed information, store the details fetched"""

    with session:

        data = {
            'schemaname': schema_name,
            'name': party_name,
            'answer': captcha_number,
            'submit11': 'Search'
        }
        headers = {
            'content-type': 'application/x-www-form-urlencoded'
        }
        headers |= HEADERS

        try:
            resp = session.post(BASE_URL, headers=headers, data=data)

            # parse response to bs4 object
            parsed_content = parse_html_content(resp.content)

            return p_html.parse_detailed_info_urls_list(parsed_content)

        except RequestException as re:
            print(f'could not make request, error: {re}')
            return None


def fetch_detailed_case_info(session: requests.Session, detailed_data_url_list: List[str]):
    """fetch and gather detailed info from the detailed info urls"""

    detailed_info_base_url = 'https://drt.gov.in/drtlive/Misdetailreport.php?no='

    detailed_case_data_list = []
    try:
        for detailed_url in detailed_data_url_list[:5]:
            response = session.get(detailed_info_base_url + detailed_url)
            parsed_content = parse_html_content(response.content)

            detailed_data = p_html.parse_detailed_table_data(parsed_content)

            if detailed_data:
                detailed_case_data_list.append(detailed_data)

        return detailed_case_data_list
    except RequestException as re:
        print(f'could not fetch detailed info')
        return None


def fetch_and_save_detailed_case_data(drt_name: str, party_name: str):
    """main driver function responsible for fetching and storing information"""

    global_session = None
    detailed_data_url_list = None
    retry_count = 3
    while retry_count > 0:

        session, schema_data, captcha_number = get_site_meta_data()
        schema_name = int(schema_data[drt_name])

        # use same session for further calls
        global_session = session

        detailed_data_url_list = fetch_detailed_case_info_urls(
            session=session,
            captcha_number=captcha_number,
            schema_name=schema_name,
            party_name=party_name
        )

        if detailed_data_url_list is None:
            retry_count -= 1
        else:
            break

    if detailed_data_url_list:
        detailed_case_data = fetch_detailed_case_info(
            session=global_session,
            detailed_data_url_list=detailed_data_url_list
        )

        # save detailed case data in excel
        if detailed_case_data:
            save_case_data_in_excel_and_csv(detailed_case_data, drt_name)
