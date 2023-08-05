import { View } from "backbone";

const EditForm = View.extend({
  initialize() {
    this.initializeElements();
    this.addEventListeners();
  },

  initializeElements() {
    this.submit = document.querySelector("input[type=submit]:not([name=modify]).button--primary");
  },

  addEventListeners() {
    if (this.submit) {
      this.submit.addEventListener("click", this.handleSubmit.bind(this));
    }
  },

  handleSubmit() {
    if (this.$el[0].checkValidity() === true) {
      this.submit.classList.add("button--disabled");
      this.submit.setAttribute("disabled", true);
      this.$el[0].submit();
    }
  },
});

export default EditForm;
