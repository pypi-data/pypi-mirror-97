import { View } from 'backbone';
import Modal from 'helpers/Modal';

const SelectApi = View.extend({
  /**
   * Backbone Init Setter
   */
  initialize() {
    this.$el.removeClass('api-select');
    const input = this.$el.find('input');
    this.label = $(`label[for="${input.attr('id')}"]`);
    this.placeholder = this.label.text() || 'one';
    this.name = input.attr('name');
    this.url = this.$el.data('api');
    this.addUrl = this.$el.data('add');
    this.isLoading = false;
    this.isMultiple = input.is('[data-multiple]');
    this.selectize = null;
    this.selected = this.gatherSelected();
    if (!this.isMultiple) {
      this.singleInput = $(input[0]).clone();
    }

    const id = input[0].defaultValue
    this.baseApiUrl = this.$el.data('base-api')
    this.setEditUrl(id)
    if (this.addUrl) {
      this.editButton = this.createButton("edit")
      this.createButton("add")
    }
  },

  /**
   * Render Views
   */
  render() {
    let opts;
    const baseOpts = {
      placeholder: `Select ${this.placeholder}`,
      valueField: 'text',
      labelField: 'text',
      searchField: 'text',
      create: this.create.bind(this),
      onItemAdd: this.addItem.bind(this),
      load: this.load.bind(this),
      render: this.renderOption(this.isLoading),
      onInitialize: this.initSelections.bind(this),
      onChange: this.onChange.bind(this),
    };
    if (this.isMultiple) {
      opts = Object.assign(baseOpts, {
        plugins: ['restore_on_backspace', 'remove_button'],
        onItemRemove: this.removeItem.bind(this),
      });
    } else {
      opts = Object.assign(baseOpts, {
        preload: 'focus',
        maxItems: 1,
      });
    }
    this.$el.selectize(opts);
  },

  /**
   * Set selections based on server rendered data
   */
  initSelections() {
    this.selectize = this.$el[0].selectize;
    for (const item of this.selected) {
      this.selectize.addOption(item);
      this.selectize.addItem(item.value);
    }
    if (!this.isMultiple) {
      this.selectize.$input.after(this.singleInput);
    }
    if (this.isEditButtonVisible()){
      this.updateEditButtonTxt()
    }
  },

  /**
   * Prepare Selectize options
   * @return {object}
   */
  renderOption (isLoading) {
    return {
      item: (item, escape) => {
        return `<div class="item" data-id="${item.id}" >${escape(item.text)}</div>`;
      },
      option: (item, escape) => {
        return `<div data-id=${item.id}>${escape(item.text)}</div>`;
      },
      option_create: (item, escape) => {
        return `<div class="create create--hide"><strong>Add${escape('+')}</strong> ${escape(
          this.name,
        )}</div>`;
      },
    };
  },

  /**
   * On create new select option
   * @param  {string}
   * @param  {function}
   */
  create (input, callback) {
    this.getPopupCallBack("add")(input)
  },

  /**
   * Load Data
   * @param  {string}  input query
   * @param  {Function}  callback function
   * @return {function}  return callback
   */
  load (query, callback) {
    if (!query.length && this.isMultiple) return callback();
    this.isLoading = true;
    $.ajax({
      url: `${this.url}&page=1&search=${encodeURIComponent(query)}`,
      type: 'GET',
      dataType: 'json',
      error: () => {
        callback();
      },
      success: response => {
        this.isLoading = false;
        const results = this.transformResults(response);
        if (!results.length) {
          $('.create.create--hide').removeClass('create--hide');
        }
        callback(response.results);
      },
    });
  },

  /**
   * On Add New Item to multi select
   * @param {string}
   * @param {object}
   */
  addItem (value, $item) {
    if (this.isMultiple) {
      if(value){
        const id = $item.attr('data-id')
        this.updateEditButton(id)
        this.selectize.$input.after(
          $('<input />', {
            name: this.name,
            value: id,
            'data-title': $item.attr('data-value'),
            type: 'hidden',
          }),
        );
      }
    } else if ($item.attr('data-id') !== this.singleInput.val()) {
       this.updateEditButton($item.attr('data-id'))
      this.singleInput.val($item.attr('data-id'));
    }
  },

  getPopupCallBack(btn_type){
    return (tag) => {
      let url = (btn_type === "add") ? this.addUrl : this.editUrl
      let modal = new Modal(url, `modal-${btn_type}-` + this.name, false, (data) => {
        let item = {
          id: data.id,
          text: data.text,
          value: data.text
        }
        if (btn_type === "edit"){
          this.selectize.removeOption(this.selectize.getValue())
          this.selectize.removeItem(this.selectize.getValue())
        }
        this.selectize.addOption(item)
        this.selectize.addItem(item.value, false)
        if (this.shouldShowEditButton()){
          this.editButton.show()
          this.updateEditButton(data.id)
        }
      }, (data) => {
        this.selectize.unlock()
      })
      if (typeof tag == 'string') {
        modal.open(tag)
      } else {
        modal.open()
      }
      return false
    }
  },

  /**
   * On Removing selected item in multi select
   * @param  {string}
   */
  removeItem (value) {
    this.selectize.$input.siblings(`[data-title="${value}"]`).remove();
  },

  /**
   * Transform Response Data
   * @param  {object}
   * @return {object}
   */
  transformResults (response) {
    this.fields = [];
    this.params = [];

    for (const param in response.params) {
      this.param = this.param || param;
      this.params.push({
        id: param,
        name: response.params[param].label,
      });
    }

    for (const field in response.fields) {
      this.fields.push(field);
    }

    return response.results.map(item => {
      item.text = this.createText(item, this.fields);
      return item;
    });
  },

  /**
   * Built text field from all fields
   * @param  {object}
   * @param  {array}
   * @return {string}
   */
  createText(item, fields) {
    const text = [];

    for (const field of fields) {
      text.push(item[field]);
    }

    return text.join(' - ');
  },

  /**
   * Append 'add' or 'edit' button to add/edit object in popup
   */
  createButton(btn_type){
    let url = (btn_type === "add") ? this.addUrl : this.editUrl
    const capitalized_btn_type = btn_type[0].toUpperCase() + btn_type.substring(1)
    const button = $('<a>')
      .attr('href', url)
      .addClass(`button button--primary formset__button--${btn_type}`)
      .html(`<i class="fa fa-plus-circle" aria-hidden="true"></i> ${capitalized_btn_type} ${this.placeholder}`);
    if (btn_type === "edit" && !this.shouldShowEditButton()){
      button.hide()
    }
    this.$el.after(button).parent().addClass(`formset__field--has-${btn_type}-button`);
    button.on('click', this.getPopupCallBack(btn_type).bind(this));
    return button

  },

  setEditUrl(id){
    this.editUrl = `${this.baseApiUrl}${id}/edit/?popup=1`
  },

   onChange(){
     if (this.shouldShowEditButton()){
       this.editButton.show()
     }
     if (this.isEditButtonVisible()){
       const id = this.$el.siblings(".selectize-control.single").find(".item").data("id")
       this.updateEditButton(id)
     }
  },

  updateEditButton(id){
    if (this.isEditButtonVisible()){
      this.updateEditLinks(id)
      this.updateEditButtonTxt()
    }
  },

  updateEditButtonTxt(){
    this.editButton.text(`Edit ${this.selectize.getValue()}:`)
  },

  updateEditLinks(id){
    this.setEditUrl(id)
    this.editButton.attr("href", this.editUrl)
  },

  isEditButtonVisible(){
    return this.editButton.is(":visible")
  },

  shouldShowEditButton(){
    return Boolean(this.addUrl && !this.isMultiple && this.selectize && this.selectize.getValue())
  },

  /**
   * Gather preselected from server rendered data
   * @return {Array}
   */
  gatherSelected() {
    const data = [];
    this.$el.find(`input[name=${this.name}]`).each((key, item) => {
      const title = this.isMultiple ? $(item).data('title') : this.$el.data('title');
      if(title){
        data.push({
          id: $(item).val(),
          text: title,
          value: title,
        });
      }
    });
    return data;
  },
});

export default SelectApi;
