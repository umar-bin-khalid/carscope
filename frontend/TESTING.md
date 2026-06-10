# Testing Guide

## Overview

CarScope includes a comprehensive E2E test suite using Playwright with HAR-based network mocking for reproducible, fast tests.

## Setup

### 1. Install Dependencies

```bash
npm install
```

### 2. Build the Project

```bash
npm run build
```

## Running Tests

### All Tests (Standard E2E)

```bash
npm run test:e2e
```

Runs all tests in `tests/e2e.spec.ts`. Tests use real network calls to the backend API.

### HAR-Mocked Tests (Recommended for CI/CD)

```bash
npm run test:e2e:har
```

Runs tests with mocked API responses from HAR files. **Much faster** and doesn't depend on external APIs.

### Record New HAR Files

If the backend API changes, regenerate the HAR files:

```bash
# Ensure backend is running on localhost:8000
npm run test:e2e:har:record
```

This will record all network interactions and save them to `tests/fixtures/api-default.har`.

### Debug Mode

```bash
npm run test:e2e:debug
```

Opens Playwright Inspector for step-by-step debugging.

### UI Mode (Visual Test Runner)

```bash
npm run test:e2e:ui
```

Opens interactive test UI in your browser. Great for development.

## Test Coverage

### Main Test Suite (`tests/e2e.spec.ts`)

#### Page Load & Initial State
- ✅ Header and branding
- ✅ Filter panel display
- ✅ Chat panel with suggested questions
- ✅ Initial car listings load

#### Filter Interaction
- ✅ Filter by make, price range, mileage
- ✅ Clear filters functionality

#### Car Selection & Saved Cars
- ✅ Select/deselect cars
- ✅ Save cars to saved list
- ✅ Display selected car details panel

#### AI Agent - Tool Execution
- ✅ `list_current_cars` – Show all cars on page
- ✅ `get_vehicle_details` – Display car specs card
- ✅ `compare_cars` – Side-by-side comparison table
- ✅ `web_search` – Web search results cards
- ✅ `get_saved_cars` – Saved cars list

#### Chat Interaction
- ✅ Send messages to agent
- ✅ Tool activity rail display
- ✅ Loading state indicator
- ✅ Response formatting (cards, tables, etc.)

#### UI & Visual Elements
- ✅ LIVE badge on Marketcheck cars
- ✅ $/mile ratio display
- ✅ Image fallback handling

#### Error Handling
- ✅ Invalid filter value handling
- ✅ Agent error recovery

#### Performance
- ✅ Page loads in < 5 seconds
- ✅ Filter response within 2 seconds
- ✅ HAR-mocked requests complete in < 1.5 seconds

### HAR-Mocked Test Suite (`tests/e2e.har.spec.ts`)

Same tests as main suite but using pre-recorded network responses:
- ✅ No external API dependency
- ✅ ~10x faster execution
- ✅ Reproducible results
- ✅ Works offline

## HAR Mocking Details

### What is a HAR File?

HAR (HTTP Archive) files record HTTP interactions. Playwright can replay them for deterministic testing.

- **Benefits:**
  - Tests don't depend on real APIs
  - No rate limiting issues
  - Tests run in parallel safely
  - Perfect for CI/CD pipelines
  - Works offline

- **Location:** `tests/fixtures/api-default.har`

### Regenerating HAR Files

When backend API changes:

```bash
# 1. Ensure backend is running
cd ../backend && python -m uvicorn app.main:app --reload

# 2. In frontend directory, record new HAR
npm run test:e2e:har:record

# 3. Verify tests pass with new HAR
npm run test:e2e:har
```

## Running Tests in CI/CD

Example GitHub Actions workflow (included in `.github/workflows/test.yml`):

```yaml
- name: Install dependencies
  run: npm install

- name: Run E2E tests (HAR-mocked)
  run: npm run test:e2e:har

- name: Upload test results
  if: always()
  uses: actions/upload-artifact@v3
  with:
    name: playwright-report
    path: playwright-report/
```

## Test Results

After running tests, open the HTML report:

```bash
npx playwright show-report
```

## Tips & Best Practices

### 1. **Use HAR for CI/CD**
Always use `npm run test:e2e:har` in CI/CD for speed and reliability.

### 2. **Use Standard Tests for Development**
Use `npm run test:e2e` during local development to catch real API issues early.

### 3. **Keep HAR Files Updated**
Regenerate HAR files whenever backend API responses change.

### 4. **Test UI Changes Separately**
Visual regression tests can be added by capturing screenshots:

```typescript
test('should match snapshot', async ({ page }) => {
  await expect(page).toHaveScreenshot();
});
```

### 5. **Debug Flaky Tests**
Use `--debug` flag to step through tests:

```bash
npm run test:e2e:debug -- tests/e2e.spec.ts
```

## Troubleshooting

### Tests timeout on real API calls

**Solution:** Use HAR-mocked tests instead:
```bash
npm run test:e2e:har
```

### HAR file is outdated

**Solution:** Regenerate it:
```bash
npm run test:e2e:har:record
```

### Tests fail to start

**Solution:** Ensure backend is running:
```bash
cd ../backend && python -m uvicorn app.main:app --reload
```

### Port conflicts

**Solution:** Update `playwright.config.ts` with different port or ensure services aren't already running.

## Test Organization

```
frontend/
├── tests/
│   ├── e2e.spec.ts              # Main E2E tests (real API)
│   ├── e2e.har.spec.ts          # HAR-mocked tests (fast)
│   ├── fixtures.ts              # HAR fixture setup
│   └── fixtures/
│       └── api-default.har      # Recorded API responses
├── playwright.config.ts         # Playwright configuration
└── package.json
```

## Integration with Git Hooks

Optional: Add tests to pre-commit hooks (requires setup):

```bash
npx husky install
npx husky add .husky/pre-commit "npm run test:e2e:har"
```

---

**Questions?** Check [Playwright Documentation](https://playwright.dev)
