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

function selectPhoto() {
  return {
    show: false,
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
    post() {
      console.log("selectPhoto.post()");
      // TODO: 選択された画像をPOST
    },
  };
}
