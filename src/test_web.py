#!/usr/bin/env python3

from web import ForestPageParser


class TestForestPageParser:
    def setup_class(self):
        self.page = ForestPageParser()

    def teardown_class(self):
        pass

    def test_adjust_one_pic_url(self):
        url1 = "http://www.forestchildcare.com.au/uploads/2/3/6/6/23669552/img-2295.jpg"

        url2 = "/uploads/2/3/6/6/23669552/img-2295.jpg"

        url3 = "/uploads/2/3/6/6/23669552/img-2295.jpg"

        url4 = "http://www.forestchildcare.com.au/files/theme/popup250_img1.jpg"

        fin_url1 = self.page.adjust_one_pic_url(url1)

        assert fin_url1 == url1

        fin_url1 = self.page.adjust_one_pic_url(url2)

        assert fin_url1 == url1

        fin_url1 = self.page.adjust_one_pic_url(url3)

        assert fin_url1 == url1

        fin_url1 = self.page.adjust_one_pic_url(url4)

        assert fin_url1 == None
