/*
 * Copyright 2013 Netherlands eScience Center
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package nl.esciencecenter.amuse.distributed.jobs;

import ibis.ipl.Ibis;
import ibis.ipl.ReadMessage;
import ibis.ipl.WriteMessage;

import java.io.IOException;

import nl.esciencecenter.amuse.distributed.DistributedAmuseException;

/**
 * @author Niels Drost
 * 
 */
public class FunctionJob extends AmuseJob {

    public FunctionJob(FunctionJobDescription description, Ibis ibis, JobSet jobManager) throws DistributedAmuseException {
        super(description, ibis, jobManager);
    }

    private String result = null;

    /**
     * @return the result
     * 
     * @throws DistributedAmuseException
     *             in case the job failed for some reason
     */
    public synchronized String getResult() throws DistributedAmuseException {

        waitUntilDone();

        if (hasFailed()) {
            throw new DistributedAmuseException("Error while running job " + this, getError());
        }

        return result;
    }

    /**
     * @param writeMessage
     * @throws IOException
     */
    @Override
    void writeJobData(WriteMessage writeMessage) throws IOException {
        //NOTHING, NO DATA ATTACHED TO FUNCTION JOB
    }

    /**
     * @param readMessage
     * @throws ClassNotFoundException
     * @throws IOException
     */
    @Override
    void readJobResult(ReadMessage readMessage) throws ClassNotFoundException, IOException {
        // TODO Auto-generated method stub

    }

}
