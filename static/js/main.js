const DEBUG_MODE = window.location.href.indexOf("nuricame") <= 0;

const url = window.URL || window.webkitURL;
const fileInput = document.getElementById("file-input");
const imagePreview = document.getElementById("image-preview");
const modalPreview = Bulma.create("modal", {
  element: document.querySelector("#modal-preview"),
});

const trace = (s) => {
  if (DEBUG_MODE && this.console && typeof console.log != "undefined") {
    console.log(s);
  }
};

const selectPhoto = () => {
  return {
    loading: false,
    startLoading() {
      trace("selectPhoto.startLoading()");
      this.loading = true;
    },
    isLoading() {
      trace("selectPhoto.isLoading()");
      return this.loading;
    },
    openPreview() {
      trace("selectPhoto.openPreview()");
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

const showResult = () => {
  return {
    isPwa() {
      return window.navigator.standalone;
    },
  };
}
