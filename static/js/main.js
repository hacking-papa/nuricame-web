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
    post(dummy_post = false) {
      trace("selectPhoto.post()");
      const params = new FormData();
      if (!dummy_post) {
        params.append("image", fileInput.files[0]);
      }
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

          const errorStatus = [400, 415];
          if (!errorStatus.includes(error.response.status)) {
            this.createAlert();
          } else {
            const reader = new FileReader();
            reader.readAsText(error.response.data);
            reader.onload = () => {
              trace(reader.result);
              const json = JSON.parse(reader.result);
              let type = "danger";
              let message =
                "すこし<ruby>時間<rt>じかん</rt></ruby>がたってから、また<ruby>試<rt>ため</rt></ruby>してみてね";
              switch (json.error_code) {
                case 40000:
                  type = "danger";
                  message =
                    "イメージパラメータがありません<br />" +
                    "お<ruby>問<rt>と</rt></ruby>い<ruby>合<rt>あ</rt></ruby>わせください";
                  break;
                case 41500:
                    type = "warning";
                    message =
                      "<ruby>画像<rt>がぞう</rt></ruby>が<ruby>選<rt>えら</rt></ruby>ばれていません<br />" +
                      "もう<ruby>一度<rt>いちど</rt></ruby>はじめからやりなおしてください";
                    break;
                case 41501:
                  type = "warning";
                  message =
                    "ぬりえにできない<ruby>種類<rt>しゅるい</rt></ruby>の<ruby>画像<rt>がぞう</rt></ruby>です<br />" +
                    "<ruby>違<rt>ちが</rt></ruby>う<ruby>画像<rt>がぞう</rt></ruby>でお<ruby>試<rt>ため</rt></ruby>しください";
                  break;
              }
              this.createAlert(type, message);
            };
          }
        });
    },
    createAlert(
      type = "danger",
      message = "すこし<ruby>時間<rt>じかん</rt></ruby>がたってから、また<ruby>試<rt>ため</rt></ruby>してみてね"
    ) {
      Bulma.create("alert", {
        type: type,
        title: "しっぱい！",
        body: message,
        confirm: "わかりました",
      });
    },
  };
}
