import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ApplicationListComponent } from './application-list';

describe('ApplicationListComponent', () => {
  let component: ApplicationListComponent;
  let fixture: ComponentFixture<ApplicationListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ApplicationListComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(ApplicationListComponent);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
