from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import urlparse
from urllib.request import urlopen


main_url = 'http://kajak.org.pl'
domain = urlparse(main_url).netloc

url_queue = list()
urls_enqueued = set()


def main():
    urls_enqueued.add(main_url)
    url_queue.append(main_url)

    while len(url_queue) > 0:
        url = url_queue.pop(0)

        internal_links = fetch_page_content(url)
        for link in internal_links:
            if link.startswith('http://') or link.startswith('https://'):
                if link not in urls_enqueued:
                    urls_enqueued.add(link)
                    url_queue.append(link)


def fetch_page_content(url):
    print("page:", url)

    html_page = urlopen(url)
    soup = BeautifulSoup(html_page, features='html.parser')

    all_links = set([normalize_url(url, link) for link in extract_attribute(soup.findAll('a'), 'href') if link])
    internal_links = [link for link in all_links if is_internal(link)]
    external_links = [link for link in all_links if not is_internal(link)]
    images = extract_attribute(soup.findAll('img'), 'src')

    print_section("internal links", internal_links)
    print_section("external links", external_links)
    print_section("images", images)

    return internal_links


def print_section(title, elements):
    print("    + {}:".format(title))
    for e in elements:
        print("       - {}".format(e))


def extract_attribute(elements, attribute_name):
    return [e.get(attribute_name) for e in elements]


def is_internal(url):
    parsed = urlparse(url)
    return not parsed.netloc or parsed.netloc == domain


def normalize_url(base, url):
    url = url.split('#')[0]
    return urljoin(base, url)


if __name__ == "__main__":
    main()
