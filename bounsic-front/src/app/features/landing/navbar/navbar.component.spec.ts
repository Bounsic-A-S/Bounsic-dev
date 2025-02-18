import { ComponentFixture, TestBed } from '@angular/core/testing';
import { NavbarAppComponent } from '@app/shared/components/navbar/navbar-app.component';
describe('NavbarComponent', () => {
  let component: NavbarAppComponent;
  let fixture: ComponentFixture<NavbarAppComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [NavbarAppComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(NavbarAppComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
