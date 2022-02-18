from scrapy.spiders import Spider


class GitSpider(Spider):
    name = 'git_spider'
    # Ключ, который определяет, какие коды ответов могут быть разрешены для каждого запроса
    handle_httpstatus_list = [404, 500]
    allowed_domains = ["github.com"]
    start_urls = [f'https://github.com/']
    name_git = input('Введите название аккаунта:')
    lis = []

    def parse(self, response, **kwargs):
        yield response.follow(url=f'https://github.com/orgs/{GitSpider.name_git}/repositories?page=1',
                              callback=self.check_request)

    def check_request(self, response):
        # Проверяем, это аккаунт компании или юзера и перенаправляем на разные адреса
        if response.status in self.handle_httpstatus_list:
            yield response.follow(url=f'https://github.com/{GitSpider.name_git}?tab=repositories',
                                  callback=self.parse_link_user)
        else:
            page_count = response.css("em.current::attr(data-total-pages)").get(default="1")
            for count in range(1, int(page_count) + 1):
                # for count in range(1, 4):
                yield response.follow(url=f'https://github.com/orgs/{GitSpider.name_git}/repositories?page={count}',
                                      callback=self.parse_link_org)

    def after_404(self, response):
        """
            Ошибка 404 или Not Found («не найдено»)
            Действия при неудачном запросе
        """
        pass

    def parse_link_user(self, response):
        """
            Парсинг ссылок на репозитории для юзеров
        """
        if "Next" not in response.css("div.BtnGroup a::text").getall() and len(
                response.css("div.BtnGroup a::text").getall()) < 2:
            GitSpider.lis.extend(response.css("h3.wb-break-all a::attr(href)").getall())
            for get_repository in GitSpider.lis:
                yield response.follow(url=f'https://github.com{get_repository}', callback=self.parse_repo_git)
        else:
            GitSpider.lis.extend(response.css("h3.wb-break-all a::attr(href)").getall())
            if len(response.css("div.BtnGroup a::attr(href)").getall()) > 1:
                yield response.follow(url=response.css("div.BtnGroup a::attr(href)")[1].get(),
                                      callback=self.parse_link_user)
            else:
                yield response.follow(url=response.css("div.BtnGroup a::attr(href)").get(),
                                      callback=self.parse_link_user)

    def parse_link_org(self, response):
        """
                    Получаем ссылки на репозитории от организационных аккаунтов
        """
        for get in response.css("div.Box ul a.d-inline-block::attr(href)").getall():
            yield response.follow(url=f'https://github.com{get}', callback=self.parse_repo_git)

    def parse_repo_git(self, response):
        """
            записываем информацию которую получили
        """
        yield {
            'name-rep': response.css("strong.mr-2 a::text").get(),
            'about': response.css("p.my-3::text").get(default='None').strip(),
            'link-site': response.css('span.flex-auto a.text-bold::text').get('None'),
            'stars': response.css("a.Link--muted strong::text").getall()[0],
            'watching': response.css("a.Link--muted strong::text").getall()[1],
            'forks': response.css("a.Link--muted strong::text").getall()[2],
            'commit-count': response.css("span.d-none strong::text").get(),
            # div css-truncate css-truncate-overflow color-fg-muted
            # a commit-author user-mention
            'commit-author': response.css("div.css-truncate a.commit-author::text").get(),
            'commit-name': response.css('span.d-none a::text').get(),
            'commit-datetime': response.css('a.Link--secondary relative-time::attr(datetime)').get(),
            'release-count': response.css("h2.h4 span::text").get(default='0'),
            'release-version': response.css('div.d-flex span.mr-2::text').get(),
            'release-datetime': response.css('div.color-fg-muted relative-time::attr(datetime)').get(),
        }
