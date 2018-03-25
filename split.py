import string
import random

class Job:
    def __init__(self, data, code):
        job = {
            'data': data,
            'code': code
        }
        self.pool = Pool()
        self.data = data
        self.name = ''
        self.code = code
        self.quantum = 5
        self.job_id = ''.join([random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(6)])
        self.division = divideData(self.data, self.quantum, self.code, self.job_id)
        self.division.dividePopulatePool()
        self.completed = []
        self.completed_ids = []
        self.sub_job_ids = [x['id'].split(" - ")[1] for x in self.division.pool.pool]
        self.status = "Incomplete"
        self.finished_data = []


    def add_result(self, data, id):
        """Returns if the job is complete"""
        if id in self.completed_ids:
            return
        self.completed.append(data)
        self.completed_ids.append(id)
        if self.completed_ids == self.sub_job_ids:
            self.status = "complete"
            self.merge_results()
            return True
        return False


    def merge_results(self):
        for processed_data in self.completed:
            self.finished_data.extend(processed_data)


    def print_merge_results(self):
        for data in self.completed:
            print(data)


    def __repr__(self):
        out = ''
        for small_job in self.division.pool.pool:
            out = out + str(small_job)
            out = out + "\n"
        return out


class Pool:

    def __init__(self):
        self.pool = []
        self.top_count = 0
        self.top_max = 1


    def insertIntoPool(self, data_job):
        self.pool.append(data_job)


    def popFromPool(self):
        if self.pool:
            job = self.pool[0]
            del(self.pool[0])
            return job
        else:
            raise Exception("Pool is presently empty!!")


    def getTopJob(self):
        if self.pool:
            self.top_count += 1
            if self.top_count >- self.top_max:
                self.top_count = 0
                job = self.popFromPool()
            else:
                job = self.pool[0]
            return job
        else:
            raise Exception("Pool is presently empty!!")


class divideData:

    def __init__(self, data, quantum, code, job_id):
        """Data fed here should be loadable to memory"""
        self.pool = Pool()
        self.data = data
        self.data_size = len(data)
        self.quantum = quantum
        self.map_code = code
        self.job_id = job_id


    def dividePopulatePool(self):
        """An element of pool is a dictionary containing the data, and
        the code"""
        for i in range(self.data_size//self.quantum):
            partition = self.data[i*self.quantum: (i+1)*self.quantum]
            partition_dict = {
                'id': f"{self.job_id} - {''.join([random.SystemRandom().choice(string.ascii_letters + string.digits) for i in range(6)])}",
                'data': partition,
                'code': self.map_code,
            }
            self.pool.insertIntoPool(partition_dict)


    def returnPool(self):
        return self.pool
