import "@testing-library/jest-dom";

global.localStorage = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
  clear: jest.fn(),
};

beforeEach(() => {
  jest.clearAllMocks();
  const storage = {};

  global.localStorage.getItem = jest.fn((key) => storage[key] || null);
  global.localStorage.setItem = jest.fn((key, value) => {
    storage[key] = value;
  });
  global.localStorage.removeItem = jest.fn((key) => {
    delete storage[key];
  });
  global.localStorage.clear = jest.fn(() => {
    Object.keys(storage).forEach((key) => delete storage[key]);
  });
});
