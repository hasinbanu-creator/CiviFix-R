const { resolveImageUri } = require('../imageUri');

describe('resolveImageUri', () => {
  it('returns data URLs unchanged', () => {
    const uri = 'data:image/jpeg;base64,abc123';
    expect(resolveImageUri(uri, 'http://localhost:8000/api/v1')).toBe(uri);
  });

  it('returns http urls unchanged', () => {
    const uri = 'http://example.com/image.jpg';
    expect(resolveImageUri(uri, 'http://localhost:8000/api/v1')).toBe(uri);
  });

  it('prefixes relative paths with the API base URL', () => {
    expect(resolveImageUri('/assets/user/images/test.jpg', 'http://localhost:8000/api/v1')).toBe(
      'http://localhost:8000/api/v1/assets/user/images/test.jpg'
    );
  });
});
