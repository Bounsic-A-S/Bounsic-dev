import { formatDuration } from "@app/features/playlist/utils/format-song-duration";

describe('Unit Test - formatDuration', () => {
  it('should format single hour and minute', () => {
    expect(formatDuration('1:1')).toBe('1 hora 1 minuto');
  });

  it('should format plural correctly', () => {
    expect(formatDuration('2:3')).toBe('2 horas 3 minutos');
  });

  it('should handle zeroes', () => {
    expect(formatDuration('0:0')).toBe('0 horas 0 minutos');
  });

  it('should handle only minutes', () => {
    expect(formatDuration('0:45')).toBe('0 horas 45 minutos');
  });

  it('should handle only hours', () => {
    expect(formatDuration('5:00')).toBe('5 horas 0 minutos');
  });
});
