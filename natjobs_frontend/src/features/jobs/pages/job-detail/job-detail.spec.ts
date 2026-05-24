import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ActivatedRoute } from '@angular/router';
import { of } from 'rxjs';
import { ApplicationService } from '../../../../core/services/application.service';
import { AuthService } from '../../../../core/services/auth.service';
import { ChatService } from '../../../../core/services/chat.service';
import { JobService } from '../../../../core/services/job.service';

import { JobDetailComponent } from './job-detail';

describe('JobDetailComponent', () => {
  let component: JobDetailComponent;
  let fixture: ComponentFixture<JobDetailComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [JobDetailComponent],
      providers: [
        {
          provide: ActivatedRoute,
          useValue: {
            snapshot: {
              params: {
                id: '1',
              },
            },
          },
        },
        {
          provide: JobService,
          useValue: {
            getJob: () => of({ id: 1, title: 'Test', description: 'Desc', recruiter: 2 }),
          },
        },
        {
          provide: ApplicationService,
          useValue: {
            apply: () => of({}),
          },
        },
        {
          provide: ChatService,
          useValue: {
            createConversation: () => of({}),
          },
        },
        {
          provide: AuthService,
          useValue: {
            role: () => 'seeker',
            user: () => ({ id: 1 }),
          },
        },
      ],
    }).compileComponents();

    fixture = TestBed.createComponent(JobDetailComponent);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
