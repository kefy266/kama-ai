/**
 * KAMA AI 6.0 - Official Node.js / JavaScript SDK
 * Origin Edge Deep Neural Architecture
 */

class KamaAI {
  /**
   * @param {Object} options
   * @param {string} [options.apiUrl='https://ai.oedge.xyz']
   * @param {string} [options.apiKey]
   */
  constructor(options = {}) {
    this.apiUrl = (options.apiUrl || 'https://ai.oedge.xyz').replace(/\/$/, '');
    this.apiKey = options.apiKey || null;
  }

  getHeaders() {
    const headers = { 'Content-Type': 'application/json' };
    if (this.apiKey) {
      headers['Authorization'] = `Bearer ${this.apiKey}`;
    }
    return headers;
  }

  /**
   * Tam bilişsel metin analizi (Toksisite, Leetspeak, Siber Zorbalık, Çocuk Güvenliği)
   * @param {string} text 
   * @returns {Promise<Object>}
   */
  async analyze(text) {
    const res = await fetch(`${this.apiUrl}/api/v6/analyze`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify({ metin: text })
    });
    if (!res.ok) throw new Error(`KAMA AI Error: ${res.statusText}`);
    return await res.json();
  }

  /**
   * AI Diplomat ile metni profesyonel / yapıcı tona dönüştürme
   * @param {string} text 
   * @param {'KURUMSAL'|'ARKADAS_CANLISI'|'YAPICI'|'SAKINLESTIRICI'} tone 
   * @returns {Promise<Object>}
   */
  async rewriteDiplomat(text, tone = 'KURUMSAL') {
    const res = await fetch(`${this.apiUrl}/api/v6/diplomat`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify({ metin: text, ton: tone })
    });
    if (!res.ok) throw new Error(`KAMA AI Error: ${res.statusText}`);
    return await res.json();
  }

  /**
   * KVKK Hassas Veri Maskeleme (T.C., IBAN, Telefon, Kart)
   * @param {string} text 
   * @returns {Promise<Object>}
   */
  async maskPII(text) {
    const res = await fetch(`${this.apiUrl}/api/v6/mask-pii`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify({ metin: text })
    });
    if (!res.ok) throw new Error(`KAMA AI Error: ${res.statusText}`);
    return await res.json();
  }

  /**
   * Discord.js Bot Mesaj Moderasyon Middleware
   * Örnek: client.on('messageCreate', kama.createDiscordMiddleware({ autoDelete: true, warnUser: true }))
   */
  createDiscordMiddleware(options = { autoDelete: true, warnUser: true }) {
    return async (message) => {
      if (message.author.bot || !message.content) return;
      try {
        const result = await this.analyze(message.content);
        if (result.toksisite_skoru >= 0.7 || result.sinif === 'KUFUR' || result.sinif === 'TEHDIT') {
          if (options.autoDelete && message.deletable) {
            await message.delete();
          }
          if (options.warnUser) {
            const reply = await message.channel.send(`⚠️ <@${message.author.id}>, mesajınız **KAMA AI 6.0 Güvenlik Kalkanı** tarafından engellendi (${result.sinif}). Lütfen kurallara uyun.`);
            setTimeout(() => reply.delete().catch(() => {}), 5000);
          }
        }
      } catch (err) {
        console.error('KAMA AI Discord Middleware Hatası:', err);
      }
    };
  }
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { KamaAI };
}
