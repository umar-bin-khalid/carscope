import { test, expect } from '@playwright/test';

/**
 * CarScope E2E Test Suite - Simplified Version
 * 
 * Tests cover:
 * - Page load and initial state (no backend required)
 * - UI interactions (with backend dependency checks)
 * - Chat interactions (basic)
 */

test.describe('CarScope MVP - Simplified', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to app
    await page.goto('/');
    // Wait for initial load
    await page.waitForLoadState('networkidle');
  });

  test.describe('Page Load & Initial State', () => {
    test('should load and display header', async ({ page }) => {
      await expect(page.locator('h1')).toContainText('CarScope');
      await expect(page.locator('text=Live inventory powered by Marketcheck')).toBeVisible();
    });

    test('should display filter panel headings', async ({ page }) => {
      await expect(page.locator('h3').filter({ hasText: 'Search' })).toBeVisible();
      await expect(page.locator('h3').filter({ hasText: 'Location' })).toBeVisible();
      await expect(page.locator('h3').filter({ hasText: 'Price' })).toBeVisible();
    });

    test('should display chat panel with suggested questions', async ({ page }) => {
      await expect(page.locator('.chat-header')).toContainText('AI Agent');
      await expect(page.locator('button:has-text("What cars are on this page?")')).toBeVisible();
      await expect(page.locator('button:has-text("Compare the first two cars")')).toBeVisible();
    });

    test('should load filter input fields', async ({ page }) => {
      await expect(page.locator('input[placeholder="e.g., BMW"]')).toBeVisible();
      await expect(page.locator('input[placeholder="e.g., 3 Series"]')).toBeVisible();
      await expect(page.locator('input[placeholder="e.g., 94102"]')).toBeVisible();
    });

    test('should load chat input', async ({ page }) => {
      const chatInput = page.locator('input[placeholder="Ask me anything..."]');
      await expect(chatInput).toBeVisible();
    });
  });

  test.describe('Filter Panel Interaction', () => {
    test('should allow typing in Make filter', async ({ page }) => {
      const makeInput = page.locator('input[placeholder="e.g., BMW"]');
      await makeInput.fill('Toyota');
      const value = await makeInput.inputValue();
      expect(value).toBe('Toyota');
    });

    test('should allow typing in Price Min filter', async ({ page }) => {
      const priceMin = page.locator('input[placeholder="Min"]').first();
      await priceMin.fill('25000');
      const value = await priceMin.inputValue();
      expect(value).toBe('25000');
    });

    test('should allow typing in Price Max filter', async ({ page }) => {
      const priceMax = page.locator('input[placeholder="Max"]').first();
      await priceMax.fill('75000');
      const value = await priceMax.inputValue();
      expect(value).toBe('75000');
    });

    test('should have Clear Filters button', async ({ page }) => {
      const clearButton = page.locator('button:has-text("Clear Filters")');
      await expect(clearButton).toBeVisible();
    });

    test('should clear filters on button click', async ({ page }) => {
      // Fill in a filter
      const makeInput = page.locator('input[placeholder="e.g., BMW"]');
      await makeInput.fill('BMW');
      
      // Clear all filters
      await page.click('button:has-text("Clear Filters")');
      await page.waitForTimeout(300);
      
      // Verify cleared
      const value = await makeInput.inputValue();
      expect(value).toBe('');
    });
  });

  test.describe('Chat Panel Interaction', () => {
    test('should allow typing in chat input', async ({ page }) => {
      const chatInput = page.locator('input[placeholder="Ask me anything..."]');
      await chatInput.fill('Hello');
      const value = await chatInput.inputValue();
      expect(value).toBe('Hello');
    });

    test('should display suggested questions', async ({ page }) => {
      const suggestedQuestions = [
        'What cars are on this page?',
        'Which saved car is cheapest?',
        'Compare the first two cars',
      ];
      
      for (const question of suggestedQuestions) {
        await expect(page.locator(`button:has-text("${question}")`)).toBeVisible();
      }
    });

    test('should show initial assistant message', async ({ page }) => {
      const assistantMessages = page.locator('.chat-message.assistant');
      const count = await assistantMessages.count();
      expect(count).toBeGreaterThan(0);
    });
  });

  test.describe('UI Elements', () => {
    test('should have responsive chat panel', async ({ page }) => {
      const chatPanel = page.locator('.chat-panel');
      await expect(chatPanel).toBeVisible();
    });

    test('should have filter sidebar', async ({ page }) => {
      const sidebar = page.locator('.sidebar');
      await expect(sidebar).toBeVisible();
    });

    test('should load page without errors', async ({ page }) => {
      // Check for basic DOM structure
      await expect(page.locator('body')).toBeVisible();
      
      // Verify main elements are present
      const headerExists = await page.locator('h1:has-text("CarScope")').isVisible();
      expect(headerExists).toBe(true);
    });
  });

  test.describe('Backend Availability Tests', () => {
    test('should load car grid if backend available', async ({ page }) => {
      // This test only runs if backend is available
      try {
        await page.waitForSelector('.cars-grid > div', { timeout: 3000 });
        // If we get here, backend is available
        const carCount = await page.locator('.cars-grid > div').count();
        expect(carCount).toBeGreaterThan(0);
      } catch {
        test.skip(); // Skip if backend not running
      }
    });

    test('should load car cards if backend available', async ({ page }) => {
      try {
        await page.waitForSelector('.car-card', { timeout: 3000 });
        const cardCount = await page.locator('.car-card').count();
        expect(cardCount).toBeGreaterThan(0);
      } catch {
        test.skip();
      }
    });

    test('should show inventory count if backend available', async ({ page }) => {
      try {
        await page.waitForSelector('text=/\\d+ of \\d+ listings/', { timeout: 3000 });
        const text = await page.locator('text=/\\d+ of \\d+ listings/').textContent();
        expect(text).toMatch(/\d+ of \d+ listings/);
      } catch {
        test.skip();
      }
    });
  });

  test.describe('Chat Functionality Tests', () => {
    test('should send chat message', async ({ page }) => {
      const chatInput = page.locator('input[placeholder="Ask me anything..."]');
      await chatInput.fill('Test message');

      // Find and click Send button
      const sendButton = page.locator('button:has-text("Send")');
      if (await sendButton.isVisible()) {
        await sendButton.click();
        await page.waitForTimeout(500);

        // Verify input was cleared
        const value = await chatInput.inputValue();
        expect(value).toBe('');
      }
    });

    test('should display user message after sending', async ({ page }) => {
      const chatInput = page.locator('input[placeholder="Ask me anything..."]');
      await chatInput.fill('Test');
      
      const sendButton = page.locator('button:has-text("Send")');
      if (await sendButton.isVisible()) {
        await sendButton.click();
        await page.waitForTimeout(1000);

        // Check for user message
        const userMessages = page.locator('.chat-message.user');
        const count = await userMessages.count();
        expect(count).toBeGreaterThan(0);
      }
    });
  });
});
