/**
 * KAMA AI 1.0 Official JavaScript / Node.js SDK
 * Ultra-fast client for KAMA AI Foundation Model & Content Moderation API
 * Zero external dependencies.
 * 
 * @license MIT
 */

(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    define([], factory);
  } else if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.KamaAI = factory();
  }
}(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  class KamaClient {
    constructor(config = {}) {
      this.baseUrl = (config.baseUrl || 'http://localhost:8000').replace(/\/+$/, '');
      this.apiKey = config.apiKey || null;
      this.timeout = config.timeout || 10000;
    }

    async _request(endpoint, payload = null, method = 'POST') {
      const url = `${this.baseUrl}${endpoint}`;
      const headers = { 'Content-Type': 'application/json' };
      if (this.apiKey) {
        headers['Authorization'] = `Bearer ${this.apiKey}`;
      }

      const options = {
        method,
        headers
      };

      if (payload) {
        options.body = JSON.stringify(payload);
      }

      const controller = typeof AbortController !== 'undefined' ? new AbortController() : null;
      if (controller) {
        options.signal = controller.signal;
        setTimeout(() => controller.abort(), this.timeout);
      }

      const res = await fetch(url, options);
      if (!res.ok) {
        const text = await res.text();
        throw new Error(`[KamaAI] HTTP Error ${res.status}: ${text}`);
      }
      return await res.json();
    }

    async analyze(text) {
      return await this._request('/v1/analyze', { text });
    }

    async denetle(mesaj) {
      return await this.analyze(mesaj);
    }

    async batch(items) {
      return await this._request('/v1/batch', { items });
    }

    async diplomat(text) {
      return await this._request('/v1/diplomat', { text });
    }

    async maskPII(text) {
      return await this._request('/v1/mask-pii', { text });
    }

    async getModelInfo() {
      return await this._request('/v1/model-info', null, 'GET');
    }
  }

  return {
    version: '1.0.0',
    Client: KamaClient,
    createClient: (config) => new KamaClient(config)
  };
}));
