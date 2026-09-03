---
title: "{{ replace .File.ContentBaseName "-" " " | title }}"
date: {{ .Date }}
speaker: ""
series: ""
description: "A short summary for the guide archive and search results."
draft: true
---

<div class="dg-wrap">
  <section class="dg-card">
    <h2 class="dg-label">Message Recap</h2>
    <div class="dg-prose">
      <p>Add the message recap here.</p>
    </div>
  </section>

  <aside class="dg-big-idea">
    <div class="dg-big-idea-label">Main Idea</div>
    <blockquote>Add the guide's main idea here.</blockquote>
  </aside>

  <section class="dg-card">
    <h2 class="dg-label">Group Discussion Questions</h2>
    <ol class="dg-q-list">
      <li><span class="dg-q-num">1</span><div class="dg-q-body">Add a discussion question.</div></li>
      <li><span class="dg-q-num">2</span><div class="dg-q-body">Add another discussion question.</div></li>
    </ol>
  </section>

  <section class="dg-card dg-card--devo">
    <h2 class="dg-label">Daily Devotions</h2>
    <div class="dg-devo-tabs" role="tablist" aria-label="Daily devotions">
      <button class="dg-devo-tab active" data-day="monday">Monday</button>
      <button class="dg-devo-tab" data-day="tuesday">Tuesday</button>
      <button class="dg-devo-tab" data-day="wednesday">Wednesday</button>
      <button class="dg-devo-tab" data-day="thursday">Thursday</button>
      <button class="dg-devo-tab" data-day="friday">Friday</button>
    </div>
    <div class="dg-devo-panels">
      <section class="dg-devo-panel active" id="devo-monday"><div class="dg-prose"><p>Add Monday's devotion.</p></div></section>
      <section class="dg-devo-panel" id="devo-tuesday"><div class="dg-prose"><p>Add Tuesday's devotion.</p></div></section>
      <section class="dg-devo-panel" id="devo-wednesday"><div class="dg-prose"><p>Add Wednesday's devotion.</p></div></section>
      <section class="dg-devo-panel" id="devo-thursday"><div class="dg-prose"><p>Add Thursday's devotion.</p></div></section>
      <section class="dg-devo-panel" id="devo-friday"><div class="dg-prose"><p>Add Friday's devotion.</p></div></section>
    </div>
  </section>

  <section class="dg-card">
    <h2 class="dg-label">Spiritual Practice</h2>
    <div class="dg-practice-inner dg-prose">
      <p><strong>Practice:</strong> Add the weekly practice here.</p>
    </div>
  </section>

  <section class="dg-card">
    <h2 class="dg-label">Prayer Prompts</h2>
    <ul class="dg-prayer-list">
      <li><span class="dg-prayer-dot"></span><span>Add a prayer prompt.</span></li>
    </ul>
  </section>

  <section class="dg-card--teal">
    <h2 class="dg-label">Next Steps</h2>
    <ul class="dg-steps-list">
      <li><span class="dg-step-chip">→</span><span>Add a concrete next step.</span></li>
    </ul>
  </section>

  <section class="dg-card">
    <h2 class="dg-label">Resources</h2>
    <div class="dg-resource">
      <span class="dg-resource-bar"></span>
      <div><div class="dg-resource-name"><a href="https://example.org/">Resource name</a></div><div class="dg-resource-desc">Describe why this resource is helpful.</div></div>
    </div>
  </section>
</div>
