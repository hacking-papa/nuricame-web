const DEBUG_MODE = window.location.href.indexOf("nuricame") <= 0;

const url = window.URL || window.webkitURL;
const fileInput = document.getElementById("file-input");
const imagePreview = document.getElementById("image-preview");
const imageResult = document.getElementById("image-result");
const imageResultForPwa = document.getElementById("image-result-for-pwa");
const downloadLink = document.getElementById("download-link");
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
    loading: false,
    isPwa() {
      return window.navigator.standalone;
    },
    startLoading() {
      trace("selectPhoto.startLoading()");
      this.loading = true;
    },
    isLoading() {
      trace("selectPhoto.activeLoading()");
      return this.loading;
    },
    openPreview() {
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
  };
}
