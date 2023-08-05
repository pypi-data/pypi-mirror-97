import { View } from 'backbone';
import pubsub from 'helpers/pubsub';

const Sidebar = View.extend({
  initialize() {
    this.prefix = '';
    this.formsetTypes = [];
    this.isDraggable = false;
    this.didInitialize = true;
    this.sortMode = false;
    this.iconMap = {
      image: 'fa-picture-o',
      text: 'fa-file-text-o',
      video: 'fa-video-camera',
      link: 'fa-link',
      social: 'fa-users',
      promo: 'fa-bullhorn',
      newsletter: 'fa-newspaper-o',
      audio: 'fa-headphones',
      quote: 'fa-quote-left',
      quiz: 'fa-question',
      poll: 'fa-bar-chart',
      seo: 'fa-search',
    };
  },

  render() {
    this.$forms = $('.formset__forms');
    this.prefix = this.$el.data('prefix');
    this.setFormsetTypes();
    this.delegateEvents();
    this.bindControls();
  },

  bindControls() {
    this.$el.on('click', '.module-item', (e) => this.add($(e.target).data('value')));
  },

  delete(e) {
    const $dom = $(e.currentTarget);
    const $form = $dom.closest('.formset__form');

    $dom.find('input').attr('checked', true);

    let result = confirm("Delete?");
    if (result) {
        $form.addClass('formset__form--is-deleted');
        $form.find('.formset__order input').val(0);

        this.resort();
    }
  },

  add(formsetType) {
    const clone = $('<div>')
      .addClass('formset__form added-with-js')
      .attr('data-prefix', formsetType)
      .attr('data-module-type', '')
      .attr('data-module-name', '');
    let html = $(`.formset__form-template[data-prefix="${formsetType}"]`).html();

    html = html.replace(/(__prefix__)/g, this.count(formsetType));
    clone.html(html);

    this.$forms.append(clone);

    if (this.isDraggable) {
      clone.addClass('draggable');
    }

    if (this.formsetTypes.indexOf(formsetType) === -1) {
      this.formsetTypes.push({
        value: formsetType,
      });
    }

    this.enableSort();
    pubsub.trigger('scarlet:render');
  },

  count(formsetType) {
    return this.$(`.formset__form[data-prefix="${formsetType}"]`).length;
  },

  /** **********************************
  Sorting
  *********************************** */

  enableSort() {
    if (!this.sortMode) {
      if (this.$forms.find('.formset__order').length) {
        this.$forms.sortable({
          update: this.resort.bind(this),
          change: this._resort,
          containment: '#content',
          iframeFix: true,
          axis: 'y',
          scroll: true,
          snap: true,
          snapMode: 'outer',
          snapTolerance: -100,
        });
        this.$('.formset__form').addClass('draggable');
        this.isDraggable = true;
      }
      this.sortMode = true;
      this.resort();
    } else {
      this.$('.formset__form').removeClass('draggable');
      this.sortMode = false;
      this.resort();
    }
  },

  resort() {
    const $helper = this.$('.ui-sortable-helper');
    const $placeholder = this.$('.ui-sortable-placeholder');

    this.$forms.find('.formset__form').each(function(i) {
      const $dom = $(this);

      if ($dom.is('.was-deleted, .ui-sortable-helper')) {
        return;
      }

      if (i % 2) {
        $dom.addClass('odd');
      } else {
        $dom.removeClass('odd');
      }

      $dom.find('.formset__order input').val(i);
    });

    if ($placeholder.hasClass('odd')) {
      $helper.addClass('odd');
    } else {
      $helper.removeClass('odd');
    }

    this.updateMetadata();
  },

  minimize() {
    const self = this;
    this.enableSort();
    if (this.sortMode) {
      $('.formset__form').each(function(index, value) {
        if (!$(this).hasClass('formset__form--edit')) {
          $(this).addClass('formset__form--edit');
          $(this).css({ height: '100px' });
          const name = $(this).data('module-name');
          const type = $(this).data('module-type');

          $(this).append(
            `<h3><i class="fa ${self.iconMap[type]} " aria-hidden="true"></i>${name}</h3>`,
          );

          $(this).children().each(function() {
            if ($(this).hasClass('formset__field')) {
              $(this).css({ display: 'none' });
            }
          });
        }
      });
    } else {
      $('.formset__form').each(function(index, value) {
        $(this).css({ height: 'auto' });
        $('h3').remove();
        $(this).removeClass('formset__form--edit');
        $(this).children().each(function() {
          if ($(this).hasClass('formset__field')) {
            $(this).css({ display: 'block' });
          }
        });
      });
    }
  },

  /** **********************************
  Metadata
  *********************************** */

  setFormsetTypes() {
    $('.formset__type').each((i, el) => {
      const $el = $(el);
      this.formsetTypes.push({
        text: $el.data('text'),
        value: $el.data('prefix'),
      });
    });
  },

  updateMetadata() {
    for (let i = 0; i < this.formsetTypes.length; i++) {
      let formsetType = this.formsetTypes[i].value,
        $formset = $(`.formset__form[data-prefix=${formsetType}]`);

      $formset.each(function(n, el) {
        const $this = $(this);
        $this.find('.formset__order input').val($this.prevAll().length);
      });

      $(`#id_${formsetType}-TOTAL_FORMS`).val($formset.length);
    }
  },
});

export default Sidebar;
