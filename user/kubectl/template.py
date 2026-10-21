pkgname = "kubectl"
pkgver = "1.37.1"
pkgrel = 0
build_style = "go"
make_dir = "_output/bin"
# apply expects unexpanded git archive placeholder, diff expects gnu diff
make_check_args = [
    "-skip",
    "^(TestApplySetParentManagement|TestApplySet_ClusterScopedCustomResourceParent|TestDiffProgram)$",
    "./cmd/kubectl/...",
    "./staging/src/k8s.io/kubectl/...",
]
hostmakedepends = ["go"]
checkdepends = ["bash", "curl"]
pkgdesc = "Kubernetes command line tool"
license = "Apache-2.0"
url = "https://github.com/kubernetes/kubernetes"
source = f"{url}/archive/refs/tags/v{pkgver}.tar.gz"
sha256 = "89295ac375eb0fdfe68a0696d81be615771d6b27c7ad9bb675dc6ffd0d2ce5f3"
# generates completions with host binary
options = ["!cross"]


def init_build(self):
    date = (
        self.do(
            "date",
            "-u",
            "-r",
            str(self.source_date_epoch),
            "+%Y-%m-%dT%H:%M:%SZ",
            capture_output=True,
        )
        .stdout.decode()
        .strip()
    )
    major, minor = pkgver.split(".")[:2]
    ver = "k8s.io/component-base/version"
    self.make_build_args += [
        (
            f"-ldflags=-X {ver}.gitMajor={major}"
            f" -X {ver}.gitMinor={minor}"
            f" -X {ver}.buildDate={date}"
            f" -X {ver}.gitVersion=v{pkgver}"
            f" -X k8s.io/client-go/pkg/version.gitVersion=v{pkgver}"
        ),
        "./cmd/kubectl",
    ]


def post_build(self):
    for shell in ["bash", "fish", "zsh"]:
        with open(self.cwd / f"kubectl.{shell}", "w") as outf:
            self.do(
                f"{self.make_dir}/kubectl",
                "completion",
                shell,
                stdout=outf,
            )


def post_install(self):
    for shell in ["bash", "fish", "zsh"]:
        self.install_completion(f"kubectl.{shell}", shell)
