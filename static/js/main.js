var url = window.URL || window.webkitURL;
var fileInput = document.getElementById("file-input");
var imagePreview = document.getElementById("image-preview");
var imageResult = document.getElementById("image-result");

function selectPhoto() {
  return {
    show: false,
    loading: "",
    result_url: "",
    open() {
      console.log("selectPhoto.open()");
      this.show = true;
    },
    close() {
      console.log("selectPhoto.close()");
      this.show = false;
    },
    isOpen() {
      console.log("selectPhoto.isOpen()");
      return this.show;
    },
    startLoading() {
      console.log("selectPhoto.startLoading()");
      this.loading = "is-active";
    },
    stopLoading() {
      console.log("selectPhoto.stopLoading()");
      this.loading = "";
    },
    activeLoading() {
      console.log("selectPhoto.activeLoading()");
      return this.loading;
    },
    hasResult() {
      console.log("selectPhoto.hasImage(): " + this.result_url);
      return Boolean(this.result_url);
    },
    preview() {
      console.log("selectPhoto.preview()");
      imagePreview.src = url.createObjectURL(fileInput.files[0]);
    },
    previewAndOpen() {
      console.log("selectPhoto.previewAndOpen()");
      this.preview();
      this.open();
    },
    post() {
      console.log("selectPhoto.post()");
      var params = new FormData();
      params.append("image", fileInput.files[0]);
      console.log(params);
      axios
        .post("/", params, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
          responseType: "blob",
        })
        .then(this.startLoading())
        .then((response) => {
          var blob = new Blob([response.data], { type: "image/png" });
          this.result_url = url.createObjectURL(blob);
          imageResult.src = this.result_url;
          this.close();
          this.stopLoading();
        })
        .catch((error) => {
          console.log(error);
        });
    },
  };
}
