from ehelply_logger.Logger import Logger

from pydantic import BaseModel
from pathlib import Path
import json

from typing import Dict, List, Any

from git import Repo


class CommitAuthor(BaseModel):
    """
    Author of a commit
    """
    name: str
    email: str


class Stats(BaseModel):
    """
    File stats
    """
    insertions: int
    deletions: int
    lines: int


class TotalStats(Stats):
    """
    Overall stats
    """
    files: int


class CommitStats(BaseModel):
    """
    Stats of a commit
    """
    totals: TotalStats
    files: Dict[str, Stats]


class Commit(BaseModel):
    """
    Commit
    """
    sha: str
    message: str
    summary: str
    author: CommitAuthor
    created_at: str
    branch: str
    stats: CommitStats

    def __init__(self, **data: Any) -> None:
        if 'stats' not in data:
            data['stats'] = CommitStats(
                totals=TotalStats(insertions=0, deletions=0, lines=0, files=0),
                files={}
            )
        super().__init__(**data)


class Release(BaseModel):
    """
    Release
    """
    version: str
    name: str
    changelog: str = ""
    stats: CommitStats
    commit: Commit
    history: List[Commit] = []


class ReleasesConfig(BaseModel):
    repo_path: Path
    releases_path: Path


class ReleaseDetails(BaseModel):
    name: str
    version: str
    changelog: str = ""


class Releaser:
    def __init__(self, config: ReleasesConfig, logger: Logger = None, allow_dirty: bool = False) -> None:
        self.config = config

        self.logger: Logger = logger
        if not self.logger:
            self.logger = Logger()

        self.releases: list = []

        self.allow_dirty: bool = allow_dirty

        self.setup()

    def setup(self):
        with open(str(self.config.releases_path)) as file:
            self.releases = json.load(file)

    def make(self, release_details: ReleaseDetails) -> bool:
        repo = Repo(str(self.config.repo_path))

        if repo.is_dirty() and not self.allow_dirty:
            raise Exception("You cannot create a new microservice release when there are changes yet to be committed.")

        latest_commit = repo.head.commit
        latest_stats: dict = {"totals": latest_commit.stats.total, "files": latest_commit.stats.files}

        history: List[Commit] = []
        stats: dict = {"totals": {
            "insertions": 0,
            "deletions": 0,
            "lines": 0,
            "files": 0
        }, "files": {}}

        try:
            previous_sha = self.releases[-1]['commit']['sha']
        except:
            previous_sha = ""

        latest_rev = latest_commit.hexsha

        if len(previous_sha) > 0:
            previous_release_commit = repo.commit(previous_sha)
            previous_rev = previous_release_commit.hexsha
            rev = "{A}...{B}".format(A=latest_rev, B=previous_rev)
        else:
            rev = latest_commit.hexsha

        for commit in repo.iter_commits(rev=rev):
            commit_data = repo.commit(commit)
            commit_data_dict: dict = {
                "message": commit_data.message,
                "summary": commit_data.summary,
                "sha": commit_data.hexsha,
                "created_at": commit_data.committed_datetime.isoformat(),
                "branch": commit_data.name_rev.split(" ")[-1],
                "author": {"name": commit_data.author.name, "email": commit_data.author.email},
                "stats": {"totals": commit_data.stats.total, "files": commit_data.stats.files}
            }
            history.insert(0, Commit(**commit_data_dict))

            stats["totals"]["insertions"] += commit_data.stats.total["insertions"]
            stats["totals"]["deletions"] += commit_data.stats.total["deletions"]
            stats["totals"]["lines"] += commit_data.stats.total["lines"]

            for file_name, file_stats in commit_data.stats.files.items():
                if file_name in stats["files"]:
                    stats["files"][file_name]["insertions"] += file_stats["insertions"]
                    stats["files"][file_name]["deletions"] += file_stats["deletions"]
                    stats["files"][file_name]["lines"] += file_stats["lines"]
                else:
                    stats["files"][file_name] = {
                        "insertions": file_stats["insertions"],
                        "deletions": file_stats["deletions"],
                        "lines": file_stats["lines"]
                    }

        stats["totals"]["files"] += len(stats["files"])

        commit_data: dict = {
            "message": latest_commit.message,
            "summary": latest_commit.summary,
            "sha": latest_commit.hexsha,
            "created_at": latest_commit.committed_datetime.isoformat(),
            "branch": latest_commit.name_rev.split(" ")[-1],
            "author": {"name": latest_commit.author.name, "email": latest_commit.author.email},
            "stats": latest_stats
        }

        release_data: Release = Release(
            name=release_details.name,
            version=release_details.version,
            changelog=release_details.changelog,
            commit=Commit(**commit_data),
            history=history,
            stats=CommitStats(**stats)
        )

        self.releases.append(release_data.dict())

        with open(str(self.config.releases_path), 'w') as file:
            json.dump(self.releases, file)

        self.logger.info("Created new release.")
        self.logger.info(json.dumps(release_data.dict(), indent=2))

        return True
