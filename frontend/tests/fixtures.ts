import { test as base } from '@playwright/test';
import path from 'path';

/**
 * Test fixture for HAR-based network mocking
 * Records API responses first run, replays them on subsequent runs
 * 
 * Usage:
 *   test('should work', async ({ page, harContext }) => {
 *     // Use page normally, network calls are automatically mocked
 *   });
 */

export const test = base.extend({
  harContext: async ({ page }, use) => {
    const harPath = path.join(
      __dirname,
      `fixtures/api-${process.env.HAR_NAME || 'default'}.har`
    );

    const mode = process.env.RECORD_HAR === 'true' ? 'record' : 'replay';

    // Start recording/replaying
    await page.routeFromHAR(harPath, {
      url: /^https?:\/\/localhost:8000/,
      updateMode: mode === 'record' ? 'update' : undefined,
    });

    await use({ page, harPath });
  },
});

export { expect } from '@playwright/test';
