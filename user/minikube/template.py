pkgname = "minikube"
pkgver = "1.39.0"
pkgrel = 0
archs = ["aarch64", "x86_64"]
_commit = "7a9f6a841470a207de8cf4bafcccee0969d8ba10"
build_style = "go"
make_build_args = [
    "-ldflags="
    + f" -X k8s.io/minikube/pkg/version.version=v{pkgver}"
    + f" -X k8s.io/minikube/pkg/version.isoVersion=v{pkgver}"
    + " -X k8s.io/minikube/pkg/version.storageProvisionerVersion=v5"
    + f" -X k8s.io/minikube/pkg/version.gitCommitID={_commit}",
    "./cmd/minikube",
]
make_check_args = ["./cmd/...", "./pkg/..."]
hostmakedepends = ["go"]
checkdepends = ["bash"]
go_build_tags = ["libvirt_dlopen"]
go_check_tags = ["libvirt_dlopen"]
pkgdesc = "Tool for running Kubernetes locally"
license = "Apache-2.0"
url = "https://minikube.sigs.k8s.io"
source = f"https://github.com/kubernetes/minikube/archive/v{pkgver}.tar.gz"
sha256 = "052b5b75f5a714a2d619be69bd9826083b42515d810cf1cac591ef0835be7fd9"
# uses host binary to generate completions
options = ["!cross"]

match self.profile.arch:
    case "aarch64":
        # kvm2 driver is only supported on amd64 upstream
        depends = ["qemu-system-aarch64"]
    case "x86_64":
        depends = ["libvirt", "qemu-system-x86_64"]


def post_build(self):
    for completion in ["bash", "fish", "zsh"]:
        with open(f"{self.cwd}/minikube.{completion}", "w") as o:
            self.do("build/minikube", "completion", completion, stdout=o)


def post_install(self):
    for completion in ["bash", "fish", "zsh"]:
        self.install_completion(f"minikube.{completion}", completion)
