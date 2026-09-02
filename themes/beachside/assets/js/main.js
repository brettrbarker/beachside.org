(() => {
  const body = document.body;
  const menuButton = document.querySelector('[data-menu-toggle]');
  const menu = document.querySelector('[data-menu]');

  if (menuButton && menu) {
    menuButton.addEventListener('click', () => {
      const open = menuButton.getAttribute('aria-expanded') !== 'true';
      menuButton.setAttribute('aria-expanded', String(open));
      menu.classList.toggle('open', open);
      body.classList.toggle('menu-open', open);
    });
  }

  const announcement = document.querySelector('[data-announcement]');
  const announcementClose = document.querySelector('[data-announcement-close]');
  if (announcement && announcementClose) {
    announcementClose.addEventListener('click', () => {
      announcement.hidden = true;
      body.classList.remove('has-announcement');
    });
  }

  const dialog = document.querySelector('[data-search-dialog]');
  const searchInput = document.querySelector('[data-search-input]');
  const results = document.querySelector('[data-search-results]');
  let searchIndex;

  const closeSearch = () => {
    if (!dialog) return;
    dialog.hidden = true;
    body.classList.remove('dialog-open');
  };

  document.querySelectorAll('[data-search-open]').forEach((button) => {
    button.addEventListener('click', async () => {
      if (!dialog || !searchInput) return;
      if (menu) menu.classList.remove('open');
      if (menuButton) menuButton.setAttribute('aria-expanded', 'false');
      body.classList.remove('menu-open');
      dialog.hidden = false;
      body.classList.add('dialog-open');
      searchInput.focus();
      if (!searchIndex) {
        try {
          const response = await fetch('/index.json');
          searchIndex = await response.json();
        } catch (_) {
          searchIndex = [];
        }
      }
    });
  });

  document.querySelectorAll('[data-search-close]').forEach((button) => button.addEventListener('click', closeSearch));
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
      closeSearch();
      if (menu) menu.classList.remove('open');
      if (menuButton) menuButton.setAttribute('aria-expanded', 'false');
      body.classList.remove('menu-open');
    }
  });

  if (searchInput && results) {
    searchInput.addEventListener('input', () => {
      const query = searchInput.value.trim().toLowerCase();
      results.replaceChildren();
      if (query.length < 2) return;
      const matches = (searchIndex || []).filter((item) => `${item.title} ${item.description}`.toLowerCase().includes(query)).slice(0, 8);
      if (!matches.length) {
        const empty = document.createElement('p');
        empty.className = 'search-empty';
        empty.textContent = 'No matching pages found.';
        results.append(empty);
        return;
      }
      matches.forEach((item) => {
        const link = document.createElement('a');
        const title = document.createElement('strong');
        const description = document.createElement('span');
        link.className = 'search-result';
        link.href = item.url;
        title.textContent = item.title;
        description.textContent = item.description || '';
        link.append(title, description);
        results.append(link);
      });
    });
  }
})();
