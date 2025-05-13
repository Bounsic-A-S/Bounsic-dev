import { formatDuration } from "@app/features/playlist/utils/format-song-duration";

describe('Unit Test - formatDuration', () => {
  it('should format 1 minute 1 second', () => {
    expect(formatDuration(61)).toBe('01:01');
  });

  it('should format 2 minutes 3 seconds', () => {
    expect(formatDuration(123)).toBe('02:03');
  });

  it('should handle zero duration', () => {
    expect(formatDuration(0)).toBe('00:00');
  });

  it('should handle less than a minute', () => {
    expect(formatDuration(45)).toBe('00:45');
  });

  it('should handle full minutes with zero seconds', () => {
    expect(formatDuration(300)).toBe('05:00');
  });

  it('should return 00:00 for invalid input (NaN)', () => {
    expect(formatDuration(NaN)).toBe('00:00');
  });

  it('should return 00:00 for invalid input (not a number)', () => {
    // @ts-expect-error for test purposes
    expect(formatDuration('invalid')).toBe('00:00');
  });
});
