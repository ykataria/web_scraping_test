# web_scraping_test
Testing web scraping using python web scraping tools

main.py is the main staring file where fetch_and_save_detailed_case_data is the driver function.

#### For now following are functionality:
1. Fetch the initial meta-data like captcha, cookies etc
2. Set the session for all the subsequent requests
3. Solve the captcha with OCR digit recognition using pytesseract
4. Get the list of all supported selections from main page
5. Based on the user input fetch the information and parse detailed info urls
6. One by one fetch the detailed case info from the above step and store in ds
7. Parse the data and save data in a csv as well as in xlsx format


-----

### Scope of improvement:
1. Parsing all the data in detailed case data.
2. Adding database support rather than relying on files.
3. Exposing endpoints for better user interaction.
4. Improving the directory structure.
5. Adding better case handling and pauses while fetching data.

