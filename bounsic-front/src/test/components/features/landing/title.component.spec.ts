import { ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { LandingTextComponent } from '@app/features/landing/tittle/tittle.component';
import { TranslateModule } from '@ngx-translate/core';

describe('LandingTextComponent', () => {
    let component: LandingTextComponent;
    let fixture: ComponentFixture<LandingTextComponent>;

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            imports: [LandingTextComponent,TranslateModule.forRoot()],
        }).compileComponents();

        fixture = TestBed.createComponent(LandingTextComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should apply hovered class on mouseenter and remove it on mouseleave', () => {
        const h1 = fixture.debugElement.queryAll(By.css('h1'))[0];

        h1.triggerEventHandler('mouseenter', {});
        fixture.detectChanges();
        expect(h1.nativeElement.classList).toContain('hovered');

        h1.triggerEventHandler('mouseleave', {});
        fixture.detectChanges();
        expect(h1.nativeElement.classList).not.toContain('hovered');
    });
});
