import { View } from "backbone";
import Quill from "Quill";

const Editor = View.extend({
  render() {
    this.$quill = this.$(".editor__quill");
    this.$hiddenRte = this.$quill[0].parentNode.querySelector('.editor__hidden-rte');
    this.initEditor();
    this.addEventListeners();
  },

  initEditor() {
    this.options = {
      // debug: "info",
      modules: {
        toolbar: this.getToolbarOptions(),
      },
      placeholder: "Compose an epic...",
      theme: "snow", // Specify theme in configuration
    };

    this.editor = new Quill(this.$quill[0], this.options);
    this.setQuillContents();
  },

  getToolbarOptions() {
    // toolbar options
    this.buttons = [
      "bold",
      "italic",
      "underline",
      "strike",
      "blockquote",
    ];
    this.headings = [{ header: [1, 2, 3, 4, 5, 6, false] }];
    this.lists = [{ list: "ordered" }, { list: "bullet" }];
    this.scripts = [{ script: "sub" }, { script: "super" }];
    this.indent = [{ indent: "-1" }, { indent: "+1" }];
    this.media = ["link", "image", "video"];
    this.colors = [{ color: [] }, { background: [] }];

    // add toolbar options to normal and full media
    this.normal = [this.headings, this.lists, this.colors];
    this.fullMedia = [this.scripts, this.indent, this.media];

    // get the config from BE
    this.toolbarConfig = this.$hiddenRte.getAttribute("config")
      ? this.$hiddenRte.getAttribute("config")
      : "useMinimal";

    // assign minimal to toolbarOptions
    this.toolbarOptions = [this.buttons];

    // handle normal and full media toolbar options
    if (this.toolbarConfig === "useNormal") {
      this.toolbarOptions = this.toolbarOptions.concat(this.normal);
    } else if (this.toolbarConfig === "useFullMedia") {
      this.toolbarOptions = this.toolbarOptions.concat(
        this.normal,
        this.fullMedia
      );
    }

    // add clear formatting option
    this.toolbarOptions = this.toolbarOptions.concat([["clean"]]);

    return this.toolbarOptions;
  },

  setQuillContents() {
    this.$quill[0].querySelector(
      ".ql-editor"
    ).innerHTML = this.$hiddenRte.value;
  },

  // getQuillContents() {
  //   return this.$quill[0].querySelector(".ql-editor").innerHTML;
  // },

  addEventListeners() {
    var _this = this;
    this.editor.on("text-change", function (delta, oldDelta, source) {
      // if (source == "api") {
      //   console.log("An API call triggered this change.");
      // } else if (source == "user") {
      //   console.log("A user action triggered this change.");
      // }
      _this.$hiddenRte.value = _this.$quill[0].querySelector(
        ".ql-editor"
      ).innerHTML;
    });
  },
});

export default Editor;
