/* Keep the built-in Markdown editor and stored values, adding a disclosure. */
(() => {
  const markdown = CMS.getWidget('markdown');

  class CollapsibleMarkdown extends markdown.control {
    focus() {
      if (this.disclosure) this.disclosure.open = true;
      super.focus();
    }

    render() {
      return h('details', {
        className: 'cms-collapsible-markdown',
        ref: (element) => { this.disclosure = element; },
      },
      h('summary', {}, this.props.field.get('label', this.props.field.get('name'))),
      super.render());
    }
  }

  CMS.registerWidget('collapsible-markdown', CollapsibleMarkdown, markdown.preview, markdown.schema);
})();
