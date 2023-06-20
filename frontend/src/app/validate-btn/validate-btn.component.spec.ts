import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ValidateBtnComponent } from './validate-btn.component';

describe('ValidateBtnComponent', () => {
  let component: ValidateBtnComponent;
  let fixture: ComponentFixture<ValidateBtnComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ValidateBtnComponent]
    });
    fixture = TestBed.createComponent(ValidateBtnComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
