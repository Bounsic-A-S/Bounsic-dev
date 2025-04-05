import { ComponentFixture, TestBed } from '@angular/core/testing';
import { SongHeroComponent } from '@app/features/playlist/song_hero/song_hero.component';

describe('SongHeroComponent', () => {
  let component: SongHeroComponent;
  let fixture: ComponentFixture<SongHeroComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SongHeroComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(SongHeroComponent);
    component = fixture.componentInstance;

    component.totalSongs = 12;
    component.totalDuration = '2:30';

    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should render total songs and formatted duration', () => {
    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.textContent).toContain('12');
    expect(compiled.textContent).toContain('2 horas 30 minutos');
  });

});
