import { yupResolver } from "@hookform/resolvers/yup";
import { useForm } from "react-hook-form";
import * as yup from "yup";

import { useState } from "react";
import "./App.css";
import IssuesIcon from "./IssuesIcon";

const schema = yup
  .object({
    title: yup.string().required().min(10).max(128),
    description: yup.string().required().min(10).max(250),
  })
  .required();

function App() {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({
    resolver: yupResolver(schema),
  });

  const [duplicates, setDuplicates] = useState([]);

  const onSubmit = async (data) => {
    await fetch("http://127.0.0.1:5000/api/v1/issues/create", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });
  };

  const checkDuplicates = async (data) => {
    const result = await fetch("http://127.0.0.1:5000/api/v1/issues/read", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    }).then((response) => response.json());

    setDuplicates(
      result.sort((a, b) => {
        return b.similarity - a.similarity;
      })
    );
  };

  return (
    <div className="container">
      <h1>Implementation of Semantic Analysis on Issues</h1>
      <div className="row">
        <form className="col-md-8" onSubmit={handleSubmit(checkDuplicates)}>
          <fieldset className="form-control">
            <h2> Check Issue Duplication </h2>
          </fieldset>

          <fieldset className="form-control">
            <label htmlFor="title"> Title </label>
            <input id="title" className="form-field" placeholder="Title" {...register("title")} />
            <p className="text-capitalize text-error">{errors.title?.message}</p>
          </fieldset>

          <fieldset className="form-control">
            <label htmlFor="description"> Description </label>
            <textarea
              id="description"
              className="form-field field-text-area"
              {...register("description")}
              placeholder="description"
            />
            <p className="text-capitalize text-error">{errors.description?.message}</p>
          </fieldset>

          <fieldset className="form-control">
            <input className="form-field" type="submit" value={"Check Duplicate"} />
          </fieldset>

          {/* <fieldset className="form-control">
            <input className="form-field" onClick={checkDuplicates} type="button" value={"Check Duplicates"} />
          </fieldset> */}
        </form>

        <div className="col-md-4">
          <h2> List of Possible Duplicate Issues </h2>

          <ul className="list">
            {duplicates.length > 0 &&
              duplicates.map((duplicate) => {
                return (
                  <li key={duplicate.title} className="list-item">
                    <IssuesIcon /> <span className="list-item-title">{duplicate.title}</span> <br />
                    <span className="list-item-score">Duplicate with score of: {duplicate.similarity}</span>
                  </li>
                );
              })}

            {duplicates.length === 0 && <div>No duplicates found.</div>}
          </ul>
        </div>
      </div>
    </div>
  );
}

export default App;
