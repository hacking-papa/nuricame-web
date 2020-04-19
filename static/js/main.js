const DEBUG_MODE = window.location.href.indexOf("nuricame") <= 0;

const url = window.URL || window.webkitURL;
const fileInput = document.getElementById("file-input");
const imagePreview = document.getElementById("image-preview");
const imageResult = document.getElementById("image-result");

function trace(s) {
  if (DEBUG_MODE && this.console && typeof console.log != "undefined") {
    console.log(s);
    console.log(imageResult.src)
    console.log(window.location.href)
    console.log(document.URL)
  }
}

function selectPhoto() {
  return {
    show: false,
    loading: "",
    open() {
      trace("selectPhoto.open()");
      this.show = true;
    },
    close() {
      trace("selectPhoto.close()");
      this.show = false;
    },
    isOpen() {
      trace("selectPhoto.isOpen()");
      return this.show;
    },
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
      }
    },
    previewAndOpen() {
      trace("selectPhoto.previewAndOpen()");
      this.preview();
      this.open();
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
          this.close();
          this.stopLoading();
        })
        .catch((error) => {
          trace(error);
        });
    },
  };
}
