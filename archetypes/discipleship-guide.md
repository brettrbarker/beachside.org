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
    <p>Write the message recap in normal Markdown here. Keep it to a few paragraphs and focus on the heart of the teaching.</p>
  </div>
</section>

<aside class="dg-big-idea">
  <div class="dg-big-idea-label">Main Idea</div>
  <blockquote>Write the one-sentence takeaway that will anchor the guide.</blockquote>
</aside>

<section class="dg-card">
  <h2 class="dg-label">Group Discussion Questions</h2>
  <ol class="dg-q-list">
    <li>
      <div class="dg-q-num">1</div>
      <div class="dg-q-body">Question one for the group to discuss.</div>
    </li>
    <li>
      <div class="dg-q-num">2</div>
      <div class="dg-q-body">Question two for the group to discuss.</div>
    </li>
    <li>
      <div class="dg-q-num">3</div>
      <div class="dg-q-body">Question three for the group to discuss.</div>
    </li>
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
    <section class="dg-devo-panel active" id="devo-monday">
      <a class="dg-devo-scripture-pill" href="https://www.bible.com/" target="_blank" rel="noopener">📖 Scripture reference</a>
      <div class="dg-prose">
        <p>Write Monday's devotion in Markdown here. You can use normal paragraphs, short lists, and a reflective prompt.</p>
      </div>
    </section>
    <section class="dg-devo-panel" id="devo-tuesday">
      <a class="dg-devo-scripture-pill" href="https://www.bible.com/" target="_blank" rel="noopener">📖 Scripture reference</a>
      <div class="dg-prose">
        <p>Write Tuesday's devotion in Markdown here.</p>
      </div>
    </section>
    <section class="dg-devo-panel" id="devo-wednesday">
      <a class="dg-devo-scripture-pill" href="https://www.bible.com/" target="_blank" rel="noopener">📖 Scripture reference</a>
      <div class="dg-prose">
        <p>Write Wednesday's devotion in Markdown here.</p>
      </div>
    </section>
    <section class="dg-devo-panel" id="devo-thursday">
      <a class="dg-devo-scripture-pill" href="https://www.bible.com/" target="_blank" rel="noopener">📖 Scripture reference</a>
      <div class="dg-prose">
        <p>Write Thursday's devotion in Markdown here.</p>
      </div>
    </section>
    <section class="dg-devo-panel" id="devo-friday">
      <a class="dg-devo-scripture-pill" href="https://www.bible.com/" target="_blank" rel="noopener">📖 Scripture reference</a>
      <div class="dg-prose">
        <p>Write Friday's devotion in Markdown here.</p>
      </div>
    </section>
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
    <li><div class="dg-prayer-dot"></div><span>Pray for the posture and trust God is inviting you into.</span></li>
    <li><div class="dg-prayer-dot"></div><span>Pray for one specific area where you need to surrender control.</span></li>
  </ul>
</section>

<section class="dg-card--teal">
  <h2 class="dg-label">Next Steps</h2>
  <ul class="dg-steps-list">
    <li><div class="dg-step-chip">→</div><span>Take one concrete step this week that puts the teaching into practice.</span></li>
  </ul>
</section>

<section class="dg-card">
  <h2 class="dg-label">Resources</h2>
  <div class="dg-resource">
    <div class="dg-resource-bar"></div>
    <div>
      <div class="dg-resource-name"><a href="https://example.org/">Resource name</a></div>
      <div class="dg-resource-desc">Briefly explain why this resource is helpful.</div>
    </div>
  </div>
</section>

</div>
