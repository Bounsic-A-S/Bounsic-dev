import { ComponentFixture, TestBed } from '@angular/core/testing';
import { PlayListSongItemComponent } from '@app/features/playlist/playlist_song_item/playlist_song.component';
import { LucideAngularModule } from 'lucide-angular';

describe('PlayListSongItemComponent', () => {
  let component: PlayListSongItemComponent;
  let fixture: ComponentFixture<PlayListSongItemComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PlayListSongItemComponent, LucideAngularModule],
    }).compileComponents();

    fixture = TestBed.createComponent(PlayListSongItemComponent);
    component = fixture.componentInstance;

    // Mock inputs
    component.id = 1;
    component.title = 'Mock Song';
    component.artist = 'Mock Artist';
    component.album = 'Mock Album';
    component.duration = '3:45';
    component.imageUrl = 'mock-image-url.jpg';

    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should display title, artist, album and duration', () => {
    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.textContent).toContain('Mock Song');
    expect(compiled.textContent).toContain('Mock Artist');
    expect(compiled.textContent).toContain('Mock Album');
    expect(compiled.textContent).toContain('3:45');
  });

  it('should display the image', () => {
    const compiled = fixture.nativeElement as HTMLElement;
    const img = compiled.querySelector('img') as HTMLImageElement;
    expect(img).toBeTruthy();
    expect(img.src).toContain('mock-image-url.jpg');
  });
});
