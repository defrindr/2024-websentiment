"use strict";

/**
 * @author Defri Indra Mahardika
 * @since 2024
 * Converter CSV to Table HTML
 */

function expand(event) {
  let el = event.target;
  let expand = el.getAttribute("data-expand");
  let rawText = el.getAttribute("data-text");

  if (expand == 1) {
    let contentTd = rawText.substring(0, 250) + "...";
    el.innerHTML = contentTd;
    el.setAttribute('data-expand', 0)
  } else {
    el.innerHTML = rawText;
    el.setAttribute('data-expand', 1)
  }
}

class Csv2Table {
  _elementId = null;
  _source = null;
  _withHeader = true;
  _filter = "";
  _tableClass = "table table-hover table-striped";
  _containerClass = "table-responsive";

  /**
   * Constructor of class
   * Parameter id is container for table (html id attribute)
   * @param {any} params {
      id,
      source = '',
      withHeader = true,
      tableClass = "table table-hover table-striped",
      containerClass = "table-responsive"
    }
   */
  constructor(params) {
    if (params.id === undefined) throw new Error("Parameter id is required");
    if (params.source === undefined)
      throw new Error("Parameter source is required");

    if (params.withHeader !== undefined) {
      this._withHeader = params.withHeader;
    }

    if (params.tableClass !== undefined) {
      this._tableClass = params.tableClass;
    }

    if (params.containerClass !== undefined) {
      this.__containerClass = params.containerClass;
    }
    this._elementId = document.getElementById(params.id);
    this._source = params.source;

    // build table if source not empty
    if (params.source !== "") {
      this._build();
    }
  }

  /**
   * Update source instance
   * @param {any} params {source}
   */
  update(params) {
    if (params.source !== "") {
      this._source = params.source;
      this._build();
    }
  }

  filter(_filter) {
    this._filter = _filter;
  }

  /**
   * Fetch and build HTML Element
   */
  _build() {
    // Clean HTML Element
    this._elementId.innerHTML = "";

    this._fetchSource()
      .then((papa) => {
        this._elementId.innerHTML = this._makeHtml(papa.data);
      })
      .catch((err) => console.error(err));
  }

  /**
   * Fetch and parse CSV
   * @returns
   */
  _fetchSource() {
    const promiseFetch = new Promise((resolve, reject) => {
      fetch(this._source)
        .then((response) => response.text())
        .then((v) => resolve(Papa.parse(v)))
        .catch((err) => reject(err));
    });

    return promiseFetch;
  }

  /**
   * Generate HTML Element
   * @param {*} sources
   * @returns string of html element
   */
  _makeHtml(realSources) {
    let sources = Array.from(realSources);
    let header = "";
    if (this._withHeader) {
      let titles = sources.shift();

      let ths = [];

      for (let titleIndex = 0; titleIndex < titles.length; titleIndex++) {
        ths.push(`<th>${titles[titleIndex]}</th>`);
      }

      header = `<thead>${ths.join("")}</thead>`;
    }

    let body = "";
    let rows = [];

    for (let rowIndex = 0; rowIndex < sources.length; rowIndex++) {
      let columns = [];
      let source = sources[rowIndex];

      if (this._filter) {
        if (source[10] !== this._filter) continue;
      }

      for (let columnIndex = 0; columnIndex < source.length; columnIndex++) {
        let contentTd = source[columnIndex];
        if (contentTd.length > 250) {
          let rawTd = source[columnIndex];
          contentTd = contentTd.substring(0, 250) + "...";
          columns.push(
            `<td onclick='expand(event)' data-text="${rawTd}" data-expand='0'>${contentTd}</td>`
          );
        } else {
          columns.push(`<td >${contentTd}</td>`);
        }
      }

      rows.push(`<tr>${columns.join("")}</tr>`);
    }

    body = `<tbody>${rows.join("")}</tbody>`;

    let table = `<table class="${this._tableClass}">${header}${body}</table>`;

    return `<div class="${this._containerClass}">${table}</div>`;
  }
}
