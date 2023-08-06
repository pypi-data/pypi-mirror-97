import os, sys
import markdown2
import re
from collections import OrderedDict
try:
    curr_path = os.path.dirname(os.path.abspath(__file__))
    teedoc_project_path = os.path.abspath(os.path.join(curr_path, "..", "..", ".."))
    if os.path.basename(teedoc_project_path) == "teedoc":
        sys.path.insert(0, teedoc_project_path)
except Exception:
    pass
from teedoc import Plugin_Base
from teedoc import Fake_Logger



class Plugin(Plugin_Base):
    name = "teedoc-plugin-markdown-parser"
    desc = "markdown parser plugin for teedoc"
    defautl_config = {
        "parse_files": ["md"]
    }

    def __init__(self, config, doc_src_path, site_config, logger = None):
        '''
            @config a dict object
            @logger teedoc.logger.Logger object
        '''
        self.logger = Fake_Logger() if not logger else logger
        self.doc_src_path = doc_src_path
        self.site_config = site_config
        self.config = Plugin.defautl_config
        self.config.update(config)
        self.logger.i("-- plugin <{}> init".format(self.name))
        self.logger.i("-- plugin <{}> config: {}".format(self.name, self.config))
        self._extention = {
            "toc" : {
                "depth": config["toc_depth"] if "toc_depth" in config else 3
            },
            "metadata" : None,
            "fenced-code-blocks" : None,
            "highlightjs-lang" : None,
            "break-on-newline" : None,
            "code-friendly" : None,
            "cuddled-lists" : None,
            "footnotes" : None,
            "strike" : None,
            "spoiler" : None,
            "tables" : None,
            "task_list" : None
        }
        

    def on_parse_files(self, files):
        # result, format must be this
        result = {
            "ok": False,
            "msg": "",
            "htmls": OrderedDict()
        }
        # function parse md file is disabled
        if not "md" in self.config["parse_files"]:
            result["msg"] = "disabled markdown parse, but only support markdown"
            return result
        self.logger.d("-- plugin <{}> parse {} files".format(self.name, len(files)))
        # self.logger.d("files: {}".format(files))
        
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext.endswith("md"):
                with open(file, encoding="utf-8") as f:
                    content = f.read().strip()
                    content = self._update_link(content)
                    parser = markdown2.Markdown(extras = self._extention)
                    parser._toc_html = ""
                    html = parser.convert(content)
                    if "title" in html.metadata:
                        title = html.metadata["title"]
                    else:
                        title = ""
                    if "keywords" in html.metadata and not html.metadata["keywords"].strip() == "":
                        keywords = html.metadata["keywords"].split(",")
                    else:
                        keywords = []
                    if "tags" in html.metadata and not html.metadata["tags"].strip() == "":
                        tags = html.metadata["tags"].split(",")
                    else:
                        tags = []
                    if "desc" in html.metadata:
                        desc = html.metadata["desc"]
                    else:
                        desc = []
                    result["htmls"][file] = {
                        "title": title,
                        "desc": desc,
                        "keywords": keywords,
                        "tags": tags,
                        "body": html,
                        "toc": html.toc_html if html.toc_html else "",
                        "metadata": html.metadata,
                        "raw": content
                    }
            else:
                result["htmls"][file] = None
        result['ok'] = True
        return result
    
    def on_parse_pages(self, files):
        result = self.on_parse_files(files)
        return result

    
    def on_add_html_header_items(self):
        items = []
        items.append('<meta name="markdown-generator" content="teedoc-plugin-markdown-parser">')
        return items
    
    def _update_link(self, content):
        def re_del(c):
            ret = c[0].replace(".md", ".html") 
            ret = re.sub("README.md", "index.html", c[0], flags=re.I)
            ret = re.sub(r".md", ".html", ret, re.I)
            return ret

        content = re.sub(r'\[.*?\]\(.*?\.md\)', re_del, content, flags=re.I)
        return content

if __name__ == "__main__":
    config = {
    }
    plug = Plugin(config=config)
    res = plug.parse_files(["md_files/basic.md"])
    print(res)
    if not os.path.exists("out"):
        os.makedirs("out")
    for file, html in res["htmls"].items():
        if html:
            file = "{}.html".format(os.path.splitext(os.path.basename(file))[0])
            with open(os.path.join("out", file), "w") as f:
                f.write(html)

