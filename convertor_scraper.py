from playwright.sync_api import sync_playwright


def scrape_currency_conversion(amount, from_currency, to_currency):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto('https://www.curs.md/en')

            amount_selector = 'input[placeholder="Input sum"]'
            page.fill(amount_selector, amount)

            from_currency_selector = f'.btn.src-currency:has-text("{from_currency}")'
            page.click(from_currency_selector, force=True)

            to_currency_selector = f'.btn.tgt-currency:has-text("{to_currency}")'
            page.click(to_currency_selector, force=True)

            converted_amount = page.eval_on_selector('.tgt-sum', 'el => el.value')
            return f'{converted_amount} {to_currency}'
    except Exception as e:
        print("An error occurred", e)
        return None
