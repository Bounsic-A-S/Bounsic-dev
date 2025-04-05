import { ComponentFixture, TestBed } from '@angular/core/testing';
import { LandingNavBarComponent } from './navbar.component';
import { ApiService } from '@app/services/song.service';
import { of } from 'rxjs';
import { provideRouter } from '@angular/router';

describe('LandingNavBarComponent', () => {
  let component: LandingNavBarComponent;
  let fixture: ComponentFixture<LandingNavBarComponent>;

  const mockApiService = {
    getTest: () => of('Bounsic works in testing!'),
  };

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LandingNavBarComponent],
      providers: [
        provideRouter([]),
        { provide: ApiService, useValue: mockApiService },
      ],
    }).compileComponents();

    fixture = TestBed.createComponent(LandingNavBarComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
  it('should load datos from the API on init', () => {
    expect(component.datos).toBe('Bounsic works in testing!');
  });
  it('should toggle mobile menu', () => {
    expect(component.isMobileMenuOpen).toBe(false);
    component.toggleMobileMenu();
    expect(component.isMobileMenuOpen).toBe(true);
    component.toggleMobileMenu();
    expect(component.isMobileMenuOpen).toBe(false);
  });
});
