function takePhoto() {
  return {
    show: false,
    open() {
      console.log("takePhoto.open()");
      this.show = true;
    },
    close() {
      console.log("takePhoto.close()");
      this.show = false;
    },
    isOpen() {
      console.log("takePhoto.isOpen()");
      return this.show;
    },
  };
}

var url = window.URL || window.webkitURL;
var fileInput = document.getElementById("file-input");
var image = document.getElementById("image-preview");

function selectPhoto() {
  return {
    show: false,
    image_url: "",
    open() {
      console.log("selectPhoto.open()");
      this.show = true;
    },
    close() {
      console.log("selectPhoto.close()");
      this.show = false;
    },
    closeAndInit() {
      this.close();
      this.init();
    },
    isOpen() {
      console.log("selectPhoto.isOpen()");
      return this.show;
    },
    hasImage() {
      console.log("selectPhoto.hasImage(): " + this.image_url);
      return Boolean(this.image_url);
    },
    init() {
      console.log("selectPhoto.init()");
      this.image_url = "";
      image.src = "";
    },
    preview() {
      console.log("selectPhoto.preview()");
      this.image_url = url.createObjectURL(fileInput.files[0]);
      image.src = this.image_url;
    },
    post() {
      console.log("selectPhoto.post()");
      var params = new FormData();
      image.src = url.createObjectURL(fileInput.files[0]);

      params.append("image", fileInput.files[0]);
      console.log(params);
      axios
        .post("/", params, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
          responseType: "blob",
        })
        .then((response) => {
          var blob = new Blob([response.data], { type: "image/png" });
          this.image_url = url.createObjectURL(blob);
          image.src = this.image_url;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    download() {
      console.log("selectPhoto.download()");
      var link = document.createElement("a");
      document.body.appendChild(link);
      link.href = this.image_url;
      link.download = "nurie";
      link.click();
      document.body.removeChild(link);
    },
  };
}
