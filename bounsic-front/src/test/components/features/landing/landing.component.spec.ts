import { ComponentFixture, TestBed } from '@angular/core/testing';
import { LandingTextComponent } from '@app/features/landing/tittle/tittle.component';
import { TranslateLoader, TranslateModule, TranslateService } from '@ngx-translate/core';
import { of } from 'rxjs';

describe('LandingTextComponent with multiple languages', () => {
  let component: LandingTextComponent;
  let fixture: ComponentFixture<LandingTextComponent>;
  let translate: TranslateService;

  const translations: Record<string, any> = {
    es: {
      'BOUNSIC.LANDING.TITLE1': 'TU MÚSICA TU ESCENCIA',
      'BOUNSIC.LANDING.TITLE2': 'ESCUCHAR AHORA',
    },
    en: {
      'BOUNSIC.LANDING.TITLE1': 'YOUR MUSIC. YOUR VIBES.',
      'BOUNSIC.LANDING.TITLE2': 'TUNE IN.',
    },
    kr: {
      'BOUNSIC.LANDING.TITLE1': '당신의 음악. 당신의 분위기.',
      'BOUNSIC.LANDING.TITLE2': '지금 듣기 시작하세요.',
    },
  };

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        LandingTextComponent,
        TranslateModule.forRoot({
          loader: {
            provide: TranslateLoader,
            useValue: {
              getTranslation: (lang: string) => of(translations[lang]),
            },
          },
        }),
      ],
    }).compileComponents();

    fixture = TestBed.createComponent(LandingTextComponent);
    component = fixture.componentInstance;
    translate = TestBed.inject(TranslateService);
  });

  const testTranslations = (lang: string, expectedTitle: string, expectedSubtitle: string) => {
    it(`should render correctly in ${lang}`, () => {
      translate.use(lang);
      fixture.detectChanges();

      const compiled = fixture.nativeElement as HTMLElement;
      const titles = compiled.querySelectorAll('h1');

      expect(titles[0]?.textContent).toContain(expectedTitle);
      expect(titles[1]?.textContent).toContain(expectedSubtitle);
    });
  };

  it('should create the component', () => {
    expect(component).toBeTruthy();
  });

  testTranslations('es', 'TU MÚSICA TU ESCENCIA', 'ESCUCHAR AHORA');
  testTranslations('en', 'YOUR MUSIC. YOUR VIBES.', 'TUNE IN.');
  testTranslations('kr', '당신의 음악. 당신의 분위기.', '듣기 시작하세요.');
});
