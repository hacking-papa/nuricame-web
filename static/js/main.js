const DEBUG_MODE = window.location.href.indexOf("nuricame") <= 0;

const url = window.URL || window.webkitURL;
const fileInput = document.getElementById("file-input");
const imagePreview = document.getElementById("image-preview");
const imageResult = document.getElementById("image-result");
const modalPreview = Bulma.create("modal", {
  element: document.querySelector("#modal-preview"),
});

function trace(s) {
  if (DEBUG_MODE && this.console && typeof console.log != "undefined") {
    console.log(s);
  }
}

function selectPhoto() {
  return {
    loading: "",
    startLoading() {
      trace("selectPhoto.startLoading()");
      this.loading = "is-active";
    },
    stopLoading() {
      trace("selectPhoto.stopLoading()");
      this.loading = "";
    },
    activeLoading() {
      trace("selectPhoto.activeLoading()");
      return this.loading;
    },
    hasResult() {
      trace("selectPhoto.hasResult()");
      return imageResult.src !== window.location.href;
    },
    preview() {
      trace("selectPhoto.preview()");
      if (fileInput) {
        imagePreview.src = url.createObjectURL(fileInput.files[0]);
        modalPreview.open();
      }
    },
    closePreview() {
      trace("selectPhoto.closePreview()");
      modalPreview.close();
    },
    post() {
      trace("selectPhoto.post()");
      const params = new FormData();
      params.append("image", fileInput.files[0]);
      trace(params);
      axios
        .post("/", params, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
          responseType: "blob",
        })
        .then(this.startLoading())
        .then((response) => {
          const blob = new Blob([response.data], { type: "image/png" });
          imageResult.src = url.createObjectURL(blob);
          this.closePreview();
          this.stopLoading();
        })
        .catch((error) => {
          trace(error);
          this.closePreview();
          this.stopLoading();
          Bulma.create("alert", {
            type: "danger",
            title: "しっぱい！",
            body:
              "すこし<ruby>時間<rt>じかん</rt></ruby>がたってから、また<ruby>試<rt>ため</rt></ruby>してみてね。",
            confirm: "わかりました",
          });
        });
    },
  };
}
