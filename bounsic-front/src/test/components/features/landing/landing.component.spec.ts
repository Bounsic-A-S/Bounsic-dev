import { ComponentFixture, TestBed } from '@angular/core/testing';
import { LandingTextComponent } from '@app/features/landing/tittle/tittle.component';

describe('LandingComponent', () => {
    let component: LandingTextComponent;
    let fixture: ComponentFixture<LandingTextComponent>;

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            imports: [LandingTextComponent],
        }).compileComponents();

        fixture = TestBed.createComponent(LandingTextComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should create bounsic landing page', () => {
        expect(component).toBeTruthy();
    });

    it('should render the custom title', () => {
        const compiled = fixture.nativeElement as HTMLElement;
        const titles = compiled.querySelectorAll('h1');
        expect(titles[0]?.textContent).toContain('TU MÚSICA TU ESCENCIA');
    });

    it('should render the subtitle', () => {
        const compiled = fixture.nativeElement as HTMLElement;
        const titles = compiled.querySelectorAll('h1');
        expect(titles[1]?.textContent).toContain('ESCUCHAR AHORA');
    });
});
