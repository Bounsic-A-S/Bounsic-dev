import { ComponentFixture, TestBed } from '@angular/core/testing';
import { SongHeroComponent } from '@app/features/playlist/song_hero/song_hero.component';
import { TranslateModule } from '@ngx-translate/core';

describe('SongHeroComponent', () => {
  let component: SongHeroComponent;
  let fixture: ComponentFixture<SongHeroComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SongHeroComponent,TranslateModule.forRoot()],
    }).compileComponents();

    fixture = TestBed.createComponent(SongHeroComponent);
    component = fixture.componentInstance;

    component.totalSongs = 12;
    component.totalDuration = 330;

    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should render total songs and formatted duration', () => {
    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.textContent).toContain('12');
    expect(compiled.textContent).toContain('5:30');
  });

});
