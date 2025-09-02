import { test, expect } from '@playwright/test';

test.describe('SmartAgent E2E Tests', () => {

  test('homepage loads correctly', async ({ page }) => {
    await page.goto('http://localhost:3000');

    // Check that the main heading is visible
    await expect(page.locator('h1')).toContainText('SmartAgent');

    // Check navigation links
    await expect(page.locator('text=שיחות')).toBeVisible();
    await expect(page.locator('text=קריאות שירות')).toBeVisible();
    await expect(page.locator('text=יומן')).toBeVisible();
  });

  test('navigation works', async ({ page }) => {
    await page.goto('http://localhost:3000');

    // Click on calls link
    await page.click('text=שיחות');
    await expect(page).toHaveURL(/.*calls.*/);
  });

  test('API documentation is accessible', async ({ page }) => {
    await page.goto('http://localhost:8000/docs');

    // Check that FastAPI docs load
    await expect(page.locator('text=FastAPI')).toBeVisible();
  });

});

test.describe('API Integration Tests', () => {

  test('can register and login user', async ({ request }) => {
    // Register new user
    const registerResponse = await request.post('http://localhost:8000/auth/register', {
      data: {
        email: 'e2e@test.com',
        password: 'test123',
        full_name: 'E2E Test User',
        org_name: 'E2E Test Org'
      }
    });

    expect(registerResponse.ok()).toBeTruthy();
    const registerData = await registerResponse.json();
    expect(registerData).toHaveProperty('access_token');

    // Login with same credentials
    const loginResponse = await request.post('http://localhost:8000/auth/login', {
      data: {
        email: 'e2e@test.com',
        password: 'test123'
      }
    });

    expect(loginResponse.ok()).toBeTruthy();
    const loginData = await loginResponse.json();
    expect(loginData).toHaveProperty('access_token');
  });

  test('webhook endpoint responds correctly', async ({ request }) => {
    const webhookData = {
      recordingUrl: 'https://example.com/test.mp3',
      callSid: 'CA_test_123',
      from: '+1234567890',
      to: '+0987654321',
      startTime: '2025-08-30T12:00:00Z',
      duration: 120
    };

    const response = await request.post('http://localhost:8000/calls/webhook/twilio', {
      data: webhookData
    });

    // Expect 401 without auth, which means endpoint exists
    expect([200, 401]).toContain(response.status());
  });

});
