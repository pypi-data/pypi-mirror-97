from pyrustic.manager.misc import funcs
from pyrustic.manager import constant
from pyrustic.jasonix import Jasonix
from hubway.host.publishing_host import PublishingHost
import os
import os.path
import pkgutil


class MainHost:
    def __init__(self):
        self._login = None
        self._jasonix = None
        self._gurl = funcs.create_gurl()
        self._setup()

    @property
    def login(self):
        return self._login

    def auth(self, token):
        """
        Return: status_code, status_text, data
        data = the login if status is 200 or 304, else data is None
        """
        self._gurl.token = token
        res = "/user"
        response = self._gurl.request(funcs.get_hub_url(res))
        code = response.code
        json = response.json
        data = None
        if code == 304:
            json = response.cached_response.json
        if (code in (200, 304)) and json:
            data = json["login"]
        else:
            self._gurl.token = None
        self._login = data
        return (*response.status, data)

    def unauth(self):
        self._login = None
        self._gurl.token = None

    def rate(self):
        """
        Return: status_code, status_text, data
        data = {"limit": int, "remaining": int}
        """
        res = "/rate_limit"
        response = self._gurl.request(funcs.get_hub_url(res))
        code = response.code
        json = response.json
        data = {}
        if code == 304:
            json = response.cached_response.json
        if (code in (200, 304)) and json:
            data["limit"] = json["resources"]["core"]["limit"]
            data["remaining"] = json["resources"]["core"]["remaining"]
        return (*response.status, data)

    def repo_description(self, owner, repo):
        """
        Returns: (status_code, status_text, data)
        data = {"created_at": date, "description": str,
                "stargazers_count": int, "subscribers_count": int}
        """
        res = "/repos/{}/{}".format(owner, repo)
        response = self._gurl.request(funcs.get_hub_url(res))
        code = response.code
        json = response.json
        data = {}
        if code == 304:
            json = response.cached_response.json
        if (code in (200, 304)) and json:
            data["description"] = json["description"]
            date = json["created_at"]
            data["created_at"] = self._badass_iso_8601_date_parser(date)
            data["stargazers_count"] = json["stargazers_count"]
            data["subscribers_count"] = json["subscribers_count"]
        return (*response.status, data)

    def latest_release(self, owner, repo):
        """
        Returns: (status_code, status_text, data}
        data = {"tag_name": str, "published_at": date,
                "downloads_count": int}
        """
        res = "/repos/{}/{}/releases/latest".format(owner, repo)
        response = self._gurl.request(funcs.get_hub_url(res))
        code = response.code
        json = response.json
        data = {}
        if code == 304:
            json = response.cached_response.json
        if (code in (200, 304)) and json:
            data["tag_name"] = json["tag_name"]
            date = json["published_at"]
            data["published_at"] = self._badass_iso_8601_date_parser(date)
            data["downloads_count"] = self._downloads_counter(json)
        return (*response.status, data)

    def latest_releases_downloads(self, owner, repo, maxi=10):
        """
        Returns: (status_code, status_text, data}
        data = int, downloads count
        """
        res = "/repos/{}/{}/releases?per_page={}".format(owner, repo, maxi)
        response = self._gurl.request(funcs.get_hub_url(res))
        code = response.code
        json = response.json
        data = 0
        if code == 304:
            json = response.cached_response.json
        if (code in (200, 304)) and json:
            for release in json:
                data += self._downloads_counter(release)
        return (*response.status, data)

    def get_assets_from_dist_folder(self):
        dist_folder = os.path.join(self.target_project(),
                                   "dist")
        if not os.path.exists(dist_folder):
            return []
        assets = []
        for item in os.listdir(dist_folder):
            _, ext = os.path.splitext(item)
            if ext != ".whl":
                continue
            path = os.path.join(dist_folder, item)
            if not os.path.isfile(path):
                continue
            assets.append(item)
        assets.sort()
        assets.reverse()
        return assets

    def publishing(self, owner, repo, name,
                   tag_name, target_commitish,
                   description, prerelease, draft,
                   asset_path, asset_name, asset_label):
        """
        Return meta code, status code, status text
        meta code:
            0: temporary copy and zip operation are success
            1: failed to copy the project in temp cache
            2: failed to zip the project
        """
        # exec tests
        # exec prolog
        # publishing
        # exec epilog
        publishing_host = PublishingHost(self._gurl, owner, repo)
        data = publishing_host.publishing(name, tag_name,
                                          target_commitish,
                                          description, prerelease,
                                          draft, asset_path,
                                          asset_name, asset_label)
        return data

    def update_activity(self, operation, owner, repo):
        if operation == "add":
            if owner in self._jasonix.data:
                if not repo in self._jasonix.data[owner]:
                    self._jasonix.data[owner].append(repo)
            else:
                self._jasonix.data[owner] = [repo]
        elif operation == "delete":
            if owner in self._jasonix.data:
                if repo is None:
                    del self._jasonix.data[owner]
                else:
                    for i, cache in enumerate(self._jasonix.data[owner]):
                        if cache == repo:
                            del self._jasonix.data[owner][i]
                            break
        self._jasonix.save()

    def last_activity(self):
        return self._jasonix.data

    def target_project(self):
        jasonix = funcs.get_manager_jasonix()
        target = jasonix.data["target"]
        return target

    def about_target_project(self):
        """  Returns a dict:
        {"target": str, "project_name": str, "version": str}
        """
        target = self.target_project()
        project_name = os.path.basename(target)
        version = "0.0.1"
        data = {"target": target,
                "project_name": project_name,
                "version": version}
        about_path = os.path.join(target, "pyrustic_data", "info.json")
        if not os.path.exists(about_path):
            return data
        jasonix = Jasonix(about_path)
        cache = jasonix.data.get("project_name", "")
        if cache:
            project_name = cache
        cache = jasonix.data.get("version", "")
        if cache:
            version = cache
        data["project_name"] = project_name
        data["version"] = version
        return data

    def extract_owner_repo_from_url(self, url):
        """ Returns a tuple: (owner, repo) """

        patterns_to_wipe = ("https://", "www.", "github.com")
        for pattern in patterns_to_wipe:
            url = url.replace(pattern, "", 1)
        url = url.lstrip("/")
        url = url.rstrip("/")
        splitted = url.split("/")
        if len(splitted) == 2:
            return splitted
        else:
            return None

    def get_asset_version(self, name):
        pkg_name, version, *_ = name.split("-")
        return version

    def _setup(self):
        shared_folder = os.path.join(constant.PYRUSTIC_DATA_FOLDER, "hubway")
        shared_json_path = os.path.join(shared_folder, "hubway_shared_data.json")
        if not os.path.exists(shared_folder):
            os.makedirs(shared_folder)
        if not os.path.exists(shared_json_path):
            default_json = pkgutil.get_data("hubway",
                                            "misc/default_shared_data.json")
            with open(shared_json_path, "wb") as file:
                file.write(default_json)
        self._jasonix = Jasonix(shared_json_path)

    def _downloads_counter(self, json):
        count = 0
        for asset in json["assets"]:
            count += asset["download_count"]
        return count

    def _badass_iso_8601_date_parser(self, date):
        # YYYY-MM-DDTHH:MM:SSZ
        date = date.rstrip("Z")
        date_part, time_part = date.split("T")
        months = ("Jan", "Feb", "March", "April", "May", "June", "July",
                 "Aug", "Sept", "Oct", "Nov", "Dec")
        year, month, day = date_part.split("-")
        text = "{} {} {} at {}".format(day, months[int(month) - 1], year, time_part)
        return text

    def _exec_tests(self):
        return

    def _exec_prolog(self):
        return

    def _publishing(self):
        return

    def _exec_epilog(self):
        return
