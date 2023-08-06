import unittest

from mglib.path import (
    DocumentPath, PagePath,
)
from mglib.step import Step


class TestDocumentPath(unittest.TestCase):

    def test_document_url(self):
        doc_ep = DocumentPath(
            user_id=1,
            document_id=3,
            file_name="x.pdf"
        )
        self.assertEqual(
            doc_ep.url(),
            "docs/user_1/document_3/x.pdf"
        )

    def test_document_url_with_another_version(self):

        doc_ep = DocumentPath(
            user_id=1,
            document_id=15,
            file_name="x.pdf"
        )
        self.assertEqual(
            doc_ep.url(version=3),
            "docs/user_1/document_15/v3/x.pdf"
        )

        self.assertEqual(
            doc_ep.url(version=2),
            "docs/user_1/document_15/v2/x.pdf"
        )

    def test_document_url_none_vs_0(self):
        doc_ep = DocumentPath(
            user_id=1,
            document_id=15,
            file_name="x.pdf"
        )
        doc_ep.inc_version()  # current version = 1
        doc_ep.inc_version()  # current version = 2
        doc_ep.inc_version()  # current version = 3

        self.assertEqual(
            # with version == None, latest version of the document
            # will be returned, which is 3
            doc_ep.url(version=None),
            "docs/user_1/document_15/v3/x.pdf"
        )

        self.assertEqual(
            # with version == 0, version 0 will be provided
            # i.e. version=0 returns original doc.
            doc_ep.url(version=0),
            "docs/user_1/document_15/x.pdf"
        )

    def test_inc_version(self):
        """
        Document endpoints are now versioned.
        Initial version is 0.
        When version is 0, the "old" endpoint path applies i.e.
        version is not included in the path.
        After document is modified (blank page deleted for example),
        its version is incremented. If document version is > 0, then
        version is included in the path.
        """
        doc_ep = DocumentPath(
            user_id=1,
            document_id=3,
            file_name="x.pdf"
        )
        doc_ep.inc_version()

        self.assertEqual(
            doc_ep.url(),
            "docs/user_1/document_3/v1/x.pdf"
        )

        doc_ep.inc_version()

        self.assertEqual(
            doc_ep.url(),
            "docs/user_1/document_3/v2/x.pdf"
        )

        # however, explicit version can be forced
        # by providing an argument to url method.
        self.assertEqual(
            doc_ep.url(version=1),
            "docs/user_1/document_3/v1/x.pdf"
        )

    def test_dirname(self):
        ep = DocumentPath(
            user_id=1,
            document_id=3,
            aux_dir="results",
            file_name="x.pdf"
        )
        self.assertEqual(
            ep.dirname(),
            "results/user_1/document_3/"
        )

    def test_pages_dirname(self):
        ep = DocumentPath(
            user_id=1,
            document_id=3,
            aux_dir="results",
            file_name="x.pdf"
        )
        self.assertEqual(
            ep.pages_dirname(),
            "results/user_1/document_3/pages/"
        )


class TestPagePath(unittest.TestCase):

    def test_versioned_page_ep(self):
        doc_path = DocumentPath(
            user_id=1,
            document_id=3,
            file_name="x.pdf"
        )
        # document's version incremented
        doc_path.inc_version()

        page_ep = PagePath(
            document_path=doc_path,
            page_num=1,
            page_count=3
        )
        self.assertEqual(
            page_ep.path,
            "results/user_1/document_3/v1/pages/page_1.txt"
        )

    def test_txt_url(self):
        """
        Without any arguments
            page_ep.url() returns page_ep.txt_url()
        """
        doc_ep = DocumentPath(
            user_id=1,
            document_id=3,
            file_name="x.pdf"
        )
        page_ep = PagePath(
            document_path=doc_ep,
            page_num=1,
            step=Step(1),
            page_count=3
        )
        self.assertEqual(
            page_ep.url(),
            page_ep.txt_url()
        )

    def test_ppmroot(self):
        doc_ep = DocumentPath(
            user_id=1,
            document_id=3,
            file_name="x.pdf"
        )
        page_url = PagePath(
            document_path=doc_ep,
            page_num=1,
            step=Step(1),
            page_count=3
        )
        self.assertEqual(
            page_url.ppmroot,
            "results/user_1/document_3/pages/page_1/100/page"
        )

#    def test_hocr_exists(self):
#        local_media = os.path.join(
#            os.path.dirname(os.path.dirname(__file__)),
#            "test",
#            "media"
#        )
#        remote_ep = Endpoint("s3:/test-papermerge/")
#        local_ep = Endpoint(f"local:{local_media}")
#        doc_ep = DocumentPath(
#            remote_endpoint=remote_ep,
#            local_endpoint=local_ep,
#            user_id=1,
#            document_id=3,
#            file_name="x.pdf"
#        )
#        page_ep1 = PagePath(
#            document_ep=doc_ep,
#            page_num=1,
#            step=Step(1),
#            page_count=3
#        )
#        self.assertTrue(
#            page_ep1.hocr_exists()
#        )
#        page_ep2 = PagePath(
#            document_ep=doc_ep,
#            page_num=2,
#            step=Step(1),
#            page_count=3
#        )
#        self.assertFalse(
#            page_ep2.hocr_exists()
#        )


